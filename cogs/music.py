"""YouTube music playback cog.

Requires ffmpeg on the host (`pacman -S ffmpeg`, `apt install ffmpeg`, etc.).
"""

import asyncio
import contextlib
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Literal

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

from core import db
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
    video_id: str | None = None
    source: str = "user"  # "user" for requested tracks, "mix" for DJ Catto radio


@dataclass
class GuildPlayer:
    queue: deque[Track] = field(default_factory=deque)
    current: Track | None = None
    voice: discord.VoiceClient | None = None
    loop_mode: Literal["off", "track", "queue"] = "off"
    text_channel: discord.abc.Messageable | None = None
    dj_mode: bool = False


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
            video_id=info.get("id"),
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
        asyncio.run_coroutine_threadsafe(self._record_play(guild_id, track), self.bot.loop)
        if player.text_channel is not None:
            embed = discord.Embed(
                title="🎵 Now playing",
                description=f"[{track.title}]({track.web_url}) `{_fmt_duration(track.duration)}`",
                color=discord.Color.green(),
            )
            if track.source == "mix":
                embed.set_footer(text="🎧 added by DJ Catto radio")
            asyncio.run_coroutine_threadsafe(player.text_channel.send(embed=embed), self.bot.loop)

    async def _record_play(self, guild_id: int, track: Track) -> None:
        with contextlib.suppress(Exception):
            if not track.video_id:
                return
            user_id = track.requester.id if track.source == "user" else None
            await db.record_play(
                guild_id, user_id, track.video_id, track.title, track.source, int(time.time())
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
        # DJ Catto radio: if the queue emptied and DJ mode is on, keep it going.
        if not player.queue and player.loop_mode == "off":
            await self._maybe_autoplay(guild_id)
        self._start_next(guild_id)

    async def _maybe_autoplay(self, guild_id: int) -> None:
        player = self._player(guild_id)
        if player.voice is None or not player.voice.is_connected():
            return
        seed = player.current
        if seed is None or not seed.video_id:
            return
        if not await db.get_dj_mode(guild_id):
            return
        try:
            recent = await db.recent_play_ids(guild_id, 50)
            candidates = await asyncio.to_thread(self._mix_candidates, seed.video_id)
        except Exception as err:
            print(f"music: autoplay lookup failed: {err}")
            return
        pick = next(
            (vid for vid, _ in candidates if vid and vid != seed.video_id and vid not in recent),
            None,
        )
        if pick is None:  # everything recent (or empty) → take the first fresh candidate
            pick = next((vid for vid, _ in candidates if vid and vid != seed.video_id), None)
        if pick is None:
            return
        try:
            track = await self._extract(f"https://www.youtube.com/watch?v={pick}", self.bot.user)
        except Exception as err:
            print(f"music: autoplay extract failed: {err}")
            return
        track.source = "mix"
        player.queue.append(track)

    @staticmethod
    def _mix_candidates(video_id: str) -> list[tuple[str, str | None]]:
        """Pull a YouTube Mix (radio) playlist seeded from a video, flat + cheap."""
        opts = {**YDL_OPTS, "noplaylist": False, "extract_flat": True, "playlist_items": "1-25"}
        url = f"https://www.youtube.com/watch?v={video_id}&list=RD{video_id}"
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        entries = info.get("entries") or []
        return [(e["id"], e.get("title")) for e in entries if e and e.get("id")]

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

    @commands.hybrid_group(
        name="dj", fallback="status", description="DJ Catto radio: never-ending autoplay"
    )
    async def dj(self, ctx: commands.Context):
        """Default: show whether DJ Catto radio is on."""
        log_command(ctx)
        on = await db.get_dj_mode(ctx.guild.id)
        player = self._player(ctx.guild.id)
        desc = f"DJ Catto radio is **{'ON' if on else 'OFF'}**."
        if on:
            desc += "\nWhen the queue runs dry, I keep the music going based on what's been played."
            if player.current is None:
                desc += "\nPlay a song to seed the radio: `/music play <song>`."
        else:
            desc += "\nTurn it on with `/dj on` and the music never stops."
        await ctx.send(
            embed=discord.Embed(title="🎧 DJ Catto", description=desc, color=discord.Color.purple())
        )

    @dj.command(name="on", description="Turn on never-ending autoplay radio")
    async def dj_on(self, ctx: commands.Context):
        log_command(ctx)
        await db.set_dj_mode(ctx.guild.id, True)
        player = self._player(ctx.guild.id)
        player.dj_mode = True
        msg = "🎧 DJ Catto radio is **ON**. I'll keep the music flowing when the queue empties."
        if player.current is None:
            msg += "\nPlay something to get me started: `/music play <song>`."
        await ctx.send(msg)

    @dj.command(name="off", description="Turn off autoplay radio")
    async def dj_off(self, ctx: commands.Context):
        log_command(ctx)
        await db.set_dj_mode(ctx.guild.id, False)
        self._player(ctx.guild.id).dj_mode = False
        await ctx.send("🎧 DJ Catto radio is **OFF**. The queue will stop when it empties.")

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
