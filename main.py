# ------------------------MODULES-------------------------------------------------------------#
import json
import os
import time
from pathlib import Path

import discord
import psutil
from discord.ext import commands
from dotenv import load_dotenv

from admin import admin
from anicat import anicat
from core import db
from core.logging import configure as configure_logging
from events import events
from modules import (
    chat,
    gambler,
    gifs,
    hangman,
    help,
    image_generation,
    moderation,
    qutoes,
    roles,
    ticket,
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


@commands.command(name="vote")
async def vote(ctx):
    vote_link = "https://top.gg/bot/1108380972950491146/invite"
    embed = discord.Embed(
        title="Vote for the Bot!",
        description=f"Click [here]({vote_link}) to vote for the bot!",
        color=discord.Color.blue(),
    )
    await ctx.send(embed=embed)


@bot.tree.command(name="vote", description="use this command to vote for the bot")
async def vote_slash(interaction: discord.Interaction):
    vote_link = "https://top.gg/bot/1108380972950491146/invite"
    embed = discord.Embed(
        title="Vote for the Bot!",
        description=f"Click [here]({vote_link}) to vote for the bot!",
        color=discord.Color.blue(),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="uptime", description="displays the stats for the bot")
async def uptime_slash(interaction: discord.Interaction):
    end_time = time.time()
    uptime = end_time - start_time

    weeks, uptime = divmod(uptime, 604800)
    days, uptime = divmod(uptime, 86400)
    hours, uptime = divmod(uptime, 3600)
    minutes, seconds = divmod(uptime, 60)
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage("/")

    uptime_str = f"{int(weeks)} weeks, {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds\nCPU Usage: {cpu_percent}%, Memory Usage: {memory_usage.percent}%, Disk Usage: {disk_usage.percent}%"

    await interaction.response.send_message(f"Bot uptime: ``{uptime_str}``")


@commands.command(name="uptime")
async def uptime(ctx):
    try:
        end_time = time.time()
        uptime = end_time - start_time

        weeks, uptime = divmod(uptime, 604800)
        days, uptime = divmod(uptime, 86400)
        hours, uptime = divmod(uptime, 3600)
        minutes, seconds = divmod(uptime, 60)
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")

        uptime_str = f"{int(weeks)} weeks, {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds\nCPU Usage: {cpu_percent}%, Memory Usage: {memory_usage.percent}%, Disk Usage: {disk_usage.percent}%"
        await ctx.send(f"Bot uptime: ``{uptime_str}``")
    except Exception as err:
        await ctx.send(f"An error occurred while retrieving the uptime: {err}")


@bot.tree.command(name="test", description="This is a test for the application command")
async def test_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")


bot.add_command(vote)
bot.add_command(uptime)
bot.add_command(qutoes.quote)
bot.add_command(qutoes.devjoke)
bot.add_command(qutoes.dadjoke)
bot.add_command(qutoes.trivia)
bot.add_command(qutoes.insult)
bot.add_command(qutoes.darkmeme)
bot.add_command(qutoes.spooky)
bot.add_command(qutoes.advice)

# gmabler
bot.add_command(gambler.daily)
bot.add_command(gambler.weekly)
bot.add_command(gambler.balance)
bot.add_command(gambler.monie)
bot.add_command(gambler.bet)
bot.add_command(gambler.steal)
bot.add_command(gambler.leaderboard)
bot.add_command(gambler.give)


bot.add_command(gifs.hug)
bot.add_command(gifs.slap)
bot.add_command(gifs.kiss)
bot.add_command(gifs.lick)
bot.add_command(gifs.bite)
bot.add_command(gifs.bully)
bot.add_command(gifs.blush)
bot.add_command(gifs.cry)
bot.add_command(gifs.cuddle)
bot.add_command(gifs.smug)
bot.add_command(gifs.bonk)
bot.add_command(gifs.pat)
bot.add_command(gifs.handhold)
bot.add_command(gifs.nom)
bot.add_command(gifs.kill)
bot.add_command(gifs.wink)
bot.add_command(gifs.poke)


bot.add_command(chat.learn)
bot.add_command(chat.c)


bot.add_command(ticket.ticketsetup)
bot.add_command(ticket.deleteticket)


bot.add_command(valostats.vstats)
bot.add_command(valostats.valofight)


bot.add_command(moderation.mute)
bot.add_command(moderation.kick)
bot.add_command(moderation.ban)
bot.add_command(moderation.unmute)

bot.add_command(roles.setuprole)
bot.add_command(roles.createrole)
bot.add_command(roles.removerole)
bot.add_command(roles.deleterole)

bot.add_command(admin.ping)
bot.add_command(admin.servers)
bot.add_command(admin.info)
bot.add_command(admin.invite)
bot.add_command(admin.addai)

bot.add_command(anicat.anicat)
bot.add_command(anicat.anicatstats)
bot.add_command(anicat.anicatinfo)

bot.add_command(help.help)

bot.add_command(image_generation.ai)
bot.add_command(image_generation.aiterms)

bot.add_command(hangman.hangman)
bot.add_command(hangman.guess)


bot.run(DISCORD_KEY)
