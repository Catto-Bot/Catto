import hashlib
import json
import logging
import os
from pathlib import Path

import aiosqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

from core import db, errors
from core.logging import configure as configure_logging
from events import events

configure_logging()
load_dotenv()

DISCORD_KEY = os.getenv("DISCORD_ID")
COGS = [
    "cogs.prefix",
    "cogs.greet",
    "cogs.conf",
    "cogs.coinflip",
    "cogs.dice",
    "cogs.meme",
    "cogs.anime",
    "cogs.wyr",
    "cogs.emoji",
    "cogs.ship",
    "cogs.avatar",
    "cogs.fakeinfo",
    "cogs.roles",
    "cogs.quotes",
    "cogs.help",
    "cogs.moderation",
    "cogs.hangman",
    "cogs.gifs",
    "cogs.chat",
    "cogs.ai",
    "cogs.gambler",
    "cogs.ticket",
    "cogs.admin",
    "cogs.anicat",
    "cogs.valostats",
    "cogs.profile",
    "cogs.reminders",
    "cogs.polls",
    "cogs.music",
]


async def get_prefix(bot, message):
    if message.guild is None:
        return db.DEFAULT_PREFIX
    return await db.get_prefix(message.guild.id)


# ---- one-time JSON → DB migrations (run during setup_hook) ----


async def migrate_prefixes_json() -> None:
    path = Path("prefixes.json")
    if not path.exists():
        return
    with path.open() as f:
        prefixes = json.load(f)
    for guild_id, prefix in prefixes.items():
        await db.set_prefix(int(guild_id), prefix)


async def migrate_channel_json(filename: str, setter) -> None:
    path = Path(filename)
    if not path.exists():
        return
    with path.open() as f:
        data = json.load(f)
    for guild_id, channel_id in data.items():
        await setter(int(guild_id), int(channel_id))


async def migrate_confession_json() -> None:
    path = Path("conf.json")
    if not path.exists():
        return
    with path.open() as f:
        data = json.load(f)
    for guild_id, mention in data.items():
        channel_id = int(str(mention).strip("<#>"))
        await db.set_confession_channel(int(guild_id), channel_id)


async def migrate_ai_allowed_txt() -> None:
    path = Path("ai_allowed.txt")
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.isdigit():
            await db.add_ai_allowed(int(line))


async def migrate_gambler_json() -> None:
    path = Path("gamblerdata/catomonie.json")
    if not path.exists():
        return
    with path.open() as f:
        data = json.load(f)
    for user_id_str, w in data.items():
        user_id = int(user_id_str)
        username = w.get("Username", "")
        await db.create_wallet(user_id, username)
        wallet = await db.get_wallet(user_id)
        delta = w.get("coins", 0) - wallet["coins"]
        if delta:
            await db.update_coins(user_id, delta)
        async with aiosqlite.connect(db.DB_PATH) as conn:
            await conn.execute(
                "UPDATE wallet SET last_daily = ?, last_weekly = ?, username = ? WHERE user_id = ?",
                (
                    int(w.get("last_claimed", 0)),
                    int(w.get("last_claimed_weekly", 0)),
                    username,
                    user_id,
                ),
            )
            await conn.commit()


intents = discord.Intents.all()
intents.message_content = True


class CattoBot(commands.Bot):
    async def setup_hook(self) -> None:
        await db.init_db()
        await migrate_prefixes_json()
        await migrate_channel_json("channelgreet.json", db.set_welcome_channel)
        await migrate_channel_json("channeleave.json", db.set_leave_channel)
        await migrate_confession_json()
        await migrate_ai_allowed_txt()
        await migrate_gambler_json()
        for ext in COGS:
            await self.load_extension(ext)
        await self.auto_sync()

    def _command_signature(self) -> str:
        """A stable hash of the global slash-command tree."""
        payload = [cmd.to_dict(self.tree) for cmd in self.tree.get_commands()]
        blob = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(blob.encode()).hexdigest()

    async def auto_sync(self) -> None:
        """Register slash commands globally on startup, but only call Discord
        when the command set changed since the last sync (avoids the global
        sync rate limit on frequent restarts). Global commands take up to ~1h
        to propagate; the manual `!sync` command still does instant per-guild
        syncs when you need them immediately."""
        log = logging.getLogger("catto")
        try:
            signature = self._command_signature()
        except Exception:
            log.exception("Could not compute command signature; forcing sync")
            signature = None
        # Key the "already synced" state to THIS application id, so swapping the
        # bot token (a different application, but a reused database) always forces
        # a fresh sync instead of wrongly assuming the new bot is already synced.
        meta_key = f"command_signature:{self.application_id}"
        if signature is not None and signature == await db.get_meta(meta_key):
            log.info("Slash commands unchanged since last sync; skipping")
            return
        try:
            synced = await self.tree.sync()
        except Exception:
            log.exception("Global slash command sync failed")
            return
        if signature is not None:
            await db.set_meta(meta_key, signature)
        log.info("Auto-synced %d slash commands globally", len(synced))

    async def on_ready(self):  # type: ignore[override]
        print("The bot is ready", flush=True)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="/help"
            )
        )

    async def close(self) -> None:
        from core.http import close_session

        await close_session()
        await db.close_db()
        await super().close()


bot = CattoBot(command_prefix=get_prefix, intents=intents, help_command=None)
bot.remove_command("help")
errors.attach(bot)
events.setup(bot)

bot.run(DISCORD_KEY)
