# ------------------------MODULES-------------------------------------------------------------#
import json
import os
import time
from pathlib import Path

import discord
import psutil
from discord.ext import commands
from dotenv import load_dotenv

from core import db
from core.logging import configure as configure_logging
from events import events
from modules import (
    valostats,
)

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
]


async def get_prefix(bot, message):
    if message.guild is None:
        return db.DEFAULT_PREFIX
    return await db.get_prefix(message.guild.id)


async def migrate_prefixes_json() -> None:
    path = Path("prefixes.json")
    if not path.exists():
        return
    with path.open() as f:
        prefixes = json.load(f)
    for guild_id, prefix in prefixes.items():
        await db.set_prefix(int(guild_id), prefix)


async def dump_prefixes_json() -> None:
    """Mirror DB prefixes to prefixes.json so legacy modules keep working."""
    prefixes = await db.all_prefixes()
    with Path("prefixes.json").open("w") as f:
        json.dump({str(k): v for k, v in prefixes.items()}, f, indent=4)


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
        # set last_daily and last_weekly
        async with __import__("aiosqlite").connect(db.DB_PATH) as conn:
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


start_time = time.time()


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

    async def on_ready(self):  # type: ignore[override]
        # Ensure every joined guild has a DB prefix, then mirror to prefixes.json
        # for the legacy modules that still read the file. Remove once all
        # commands are migrated.
        for guild in self.guilds:
            if await db.get_prefix(guild.id) == db.DEFAULT_PREFIX:
                await db.set_prefix(guild.id, db.DEFAULT_PREFIX)
        await dump_prefixes_json()
        await self.tree.sync()
        print("The bot is ready", flush=True)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="!help & cattoprefix"
            )
        )

    async def close(self) -> None:
        from core.http import close_session

        await close_session()
        await super().close()


bot = CattoBot(command_prefix=get_prefix, intents=intents, help_command=None)
bot.remove_command("help")


events.setup(bot)


# async def on_message(member):
#     content = member.content.lower()
#     if content == "cattoprefix":
#         try:
#             with open('prefixes.json', 'r') as f:
#                 prefixes = json.load(f)
#                 await message.channel.send(prefixes[str(message.guild.id)] )
#         except:
#             prefixes = {}


bot.add_command(valostats.vstats)
bot.add_command(valostats.valofight)


bot.run(DISCORD_KEY)
