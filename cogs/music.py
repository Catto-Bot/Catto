"""YouTube music playback cog.

Requires ffmpeg on the host (`pacman -S ffmpeg`, `apt install ffmpeg`, etc.).
"""

import asyncio
import contextlib
from collections import deque
from dataclasses import dataclass, field
from typing import Literal

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

from core.logging import log_command

YDL_OPTS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch1",
    "source_address": "0.0.0.0",
}
FFMPEG_BEFORE = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
FFMPEG_OPTS = "-vn"


def _fmt_duration(secs: int | None) -> str:
    if not secs:
        return "?:??"
    m, s = divmod(int(secs), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


@dataclass
class Track:
    title: str
    web_url: str
    stream_url: str
    duration: int | None
    requester: discord.abc.User
    thumbnail: str | None = None


@dataclass
class GuildPlayer:
    queue: deque[Track] = field(default_factory=deque)
    current: Track | None = None
    voice: discord.VoiceClient | None = None
    loop_mode: Literal["off", "track", "queue"] = "off"
    text_channel: discord.abc.Messageable | None = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players: dict[int, GuildPlayer] = {}

    def _player(self, guild_id: int) -> GuildPlayer:
        return self.players.setdefault(guild_id, GuildPlayer())

    async def _extract(self, query: str, requester: discord.abc.User) -> Track:
        """Run yt-dlp in a thread (it's blocking) and shape the result."""

        def blocking() -> dict:
            with YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]
            return info

        info = await asyncio.to_thread(blocking)
        return Track(
            title=info.get("title", "unknown"),
            web_url=info.get("webpage_url", query),
            stream_url=info["url"],
            duration=info.get("duration"),
            requester=requester,
            thumbnail=info.get("thumbnail"),
        )

    def _start_next(self, guild_id: int) -> None:
        player = self._player(guild_id)
        if not player.queue or player.voice is None:
            player.current = None
            return
        track = player.queue.popleft()
        player.current = track
        source = discord.FFmpegPCMAudio(
            track.stream_url, before_options=FFMPEG_BEFORE, options=FFMPEG_OPTS
        )
        player.voice.play(source, after=lambda e: self._after_play(guild_id, e))
        if player.text_channel is not None:
            asyncio.run_coroutine_threadsafe(
                player.text_channel.send(
                    embed=discord.Embed(
                        title="🎵 Now playing",
                        description=f"[{track.title}]({track.web_url}) `{_fmt_duration(track.duration)}`",
                        color=discord.Color.green(),
                    )
                ),
                self.bot.loop,
            )

    def _after_play(self, guild_id: int, error: Exception | None) -> None:
        # Called on FFmpeg's reader thread; schedule the next pull on the event loop.
        asyncio.run_coroutine_threadsafe(self._on_song_end(guild_id, error), self.bot.loop)

    async def _on_song_end(self, guild_id: int, error: Exception | None) -> None:
        player = self._player(guild_id)
        if error is not None:
            print(f"music: ffmpeg error: {error}")
        if player.loop_mode == "track" and player.current:
            player.queue.appendleft(player.current)
        elif player.loop_mode == "queue" and player.current:
            player.queue.append(player.current)
        self._start_next(guild_id)

    async def _ensure_voice(self, ctx: commands.Context) -> discord.VoiceClient | None:
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("Join a voice channel first.")
            return None
        player = self._player(ctx.guild.id)
        if player.voice is None or not player.voice.is_connected():
            player.voice = await ctx.author.voice.channel.connect()
        elif player.voice.channel != ctx.author.voice.channel:
            await player.voice.move_to(ctx.author.voice.channel)
        player.text_channel = ctx.channel
        return player.voice

    @commands.hybrid_group(name="music", fallback="np", description="Music playback commands")
    async def music(self, ctx: commands.Context):
        """Default: show now playing."""
        log_command(ctx)
        player = self._player(ctx.guild.id)
        if player.current is None:
            await ctx.send("Nothing is playing. Use `/music play <song>` to start.")
            return
        t = player.current
        embed = discord.Embed(
            title="🎵 Now playing",
            description=f"[{t.title}]({t.web_url}) `{_fmt_duration(t.duration)}`",
            color=discord.Color.green(),
        )
        if t.thumbnail:
            embed.set_thumbnail(url=t.thumbnail)
        embed.set_footer(text=f"requested by {t.requester}")
        await ctx.send(embed=embed)

    @music.command(name="play", description="Play or queue a YouTube song by URL or keyword")
    async def play(self, ctx: commands.Context, *, query: str):
        log_command(ctx)
        if ctx.interaction is not None:
            await ctx.defer()
        voice = await self._ensure_voice(ctx)
        if voice is None:
            return
        try:
            track = await self._extract(query, ctx.author)
        except Exception as err:
            await ctx.send(f"Could not fetch that track: {err}")
            return
        player = self._player(ctx.guild.id)
        player.queue.append(track)
        if not voice.is_playing() and not voice.is_paused():
            self._start_next(ctx.guild.id)
            await ctx.send(f"▶ Playing **{track.title}** (`{_fmt_duration(track.duration)}`)")
        else:
            await ctx.send(
                f"➕ Queued **{track.title}** (#{len(player.queue)}, `{_fmt_duration(track.duration)}`)"
            )

    @music.command(name="queue", aliases=["q"], description="Show the upcoming queue")
    async def queue(self, ctx: commands.Context):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        lines: list[str] = []
        if player.current:
            lines.append(
                f"▶ **{player.current.title}** `{_fmt_duration(player.current.duration)}` by {player.current.requester}"
            )
        for i, t in enumerate(list(player.queue)[:20], 1):
            lines.append(f"`{i}.` {t.title} `{_fmt_duration(t.duration)}` by {t.requester}")
        if not lines:
            await ctx.send("Queue is empty.")
            return
        more = ""
        if len(player.queue) > 20:
            more = f"\n…and {len(player.queue) - 20} more"
        embed = discord.Embed(
            title=f"Queue ({len(player.queue)} pending, loop: {player.loop_mode})",
            description="\n".join(lines) + more,
            color=discord.Color.blurple(),
        )
        await ctx.send(embed=embed)

    @music.command(name="skip", aliases=["next"], description="Skip the current track")
    async def skip(self, ctx: commands.Context):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        if player.voice is None or not player.voice.is_playing():
            await ctx.send("Nothing to skip.")
            return
        player.voice.stop()  # triggers _after_play → _start_next
        await ctx.send("⏭ Skipped.")

    @music.command(name="stop", description="Stop playback and clear the queue")
    async def stop(self, ctx: commands.Context):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        player.queue.clear()
        player.current = None
        player.loop_mode = "off"
        if player.voice and player.voice.is_connected():
            player.voice.stop()
            await player.voice.disconnect()
        player.voice = None
        await ctx.send("⏹ Stopped and disconnected.")

    @music.command(name="pause", description="Pause the current track")
    async def pause(self, ctx: commands.Context):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        if player.voice and player.voice.is_playing():
            player.voice.pause()
            await ctx.send("⏸ Paused.")
        else:
            await ctx.send("Nothing playing.")

    @music.command(name="resume", description="Resume a paused track")
    async def resume(self, ctx: commands.Context):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        if player.voice and player.voice.is_paused():
            player.voice.resume()
            await ctx.send("▶ Resumed.")
        else:
            await ctx.send("Nothing paused.")

    @music.command(name="remove", description="Remove a track from the queue by 1-based index")
    async def remove(self, ctx: commands.Context, index: int):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        if index < 1 or index > len(player.queue):
            await ctx.send("Invalid index.")
            return
        track = player.queue[index - 1]
        del player.queue[index - 1]
        await ctx.send(f"🗑 Removed **{track.title}** from the queue.")

    @music.command(name="clearqueue", description="Empty the queue without stopping the current track")
    async def clearqueue(self, ctx: commands.Context):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        n = len(player.queue)
        player.queue.clear()
        await ctx.send(f"🧹 Cleared {n} track(s) from the queue.")

    @music.command(name="loop", description="Set loop mode: off | track | queue")
    async def loop(self, ctx: commands.Context, mode: str):
        log_command(ctx)
        mode = mode.lower()
        if mode not in ("off", "track", "queue"):
            await ctx.send("mode must be `off`, `track`, or `queue`.")
            return
        self._player(ctx.guild.id).loop_mode = mode
        await ctx.send(f"🔁 Loop mode → **{mode}**.")

    @music.command(name="leave", aliases=["disconnect", "dc"], description="Disconnect the bot from voice")
    async def leave(self, ctx: commands.Context):
        log_command(ctx)
        player = self._player(ctx.guild.id)
        if player.voice and player.voice.is_connected():
            await player.voice.disconnect()
        player.voice = None
        player.queue.clear()
        player.current = None
        await ctx.send("👋 Left voice.")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        # Auto-disconnect if the bot is left alone in voice.
        if member.bot:
            return
        for _guild_id, player in self.players.items():
            if player.voice is None or not player.voice.is_connected():
                continue
            channel = player.voice.channel
            humans = [m for m in channel.members if not m.bot]
            if not humans:
                await asyncio.sleep(60)
                humans = [m for m in channel.members if not m.bot]
                if not humans:
                    with contextlib.suppress(Exception):
                        await player.voice.disconnect()
                    player.voice = None
                    player.queue.clear()
                    player.current = None


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
