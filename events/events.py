import io
import os

import discord
from dotenv import load_dotenv

from core import db
from core.http import get_session
from core.welcomecard import render_leave_card, render_welcome_card

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


async def on_member_join(member):
    try:
        channel_id = await db.get_welcome_channel(member.guild.id)
        if channel_id is None:
            return
        channel = member.guild.get_channel(channel_id)
        if channel is None:
            return
        png = await render_welcome_card(member)
        file = discord.File(io.BytesIO(png), filename="welcome.png")
        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}!",
            description=f"{member.mention}, make sure to read the rules and enjoy your stay! 🐾",
            color=discord.Color.from_rgb(88, 101, 242),
        )
        embed.set_image(url="attachment://welcome.png")
        await channel.send(embed=embed, file=file)
    except Exception as e:
        print(f"welcome error: {e}")


async def on_member_remove(member):
    try:
        channel_id = await db.get_leave_channel(member.guild.id)
        if channel_id is None:
            return
        channel = member.guild.get_channel(channel_id)
        if channel is None:
            return
        png = await render_leave_card(member)
        file = discord.File(io.BytesIO(png), filename="leave.png")
        embed = discord.Embed(
            title=f"{member.display_name} has left",
            description="Hope you had a great time!",
            color=discord.Color.from_rgb(220, 110, 110),
        )
        embed.set_image(url="attachment://leave.png")
        await channel.send(embed=embed, file=file)
    except Exception as e:
        print(f"leave error: {e}")


LEVEL_THRESHOLDS = [
    (1, 1),
    (50, 2),
    (100, 3),
    (500, 4),
    (1000, 5),
    (5000, 6),
    (10000, 7),
    (20000, 8),
    (40000, 9),
    (50000, 10),
    (100000, 11),
]

LEVEL_COOLDOWN_SECS = 15
_last_counted: dict[int, float] = {}


async def on_message(message):
    if message.author.bot or message.guild is None:
        return
    content = message.content.lower()

    if content == "cattoprefix":
        prefix = await db.get_prefix(message.guild.id)
        await message.channel.send(f"The prefix set for this server is: '{prefix}'")
    elif content in ("gn", "goodnight"):
        await message.channel.send(f"GoodNight, {message.author.mention}!")
    elif content in ("gm", "goodmorning"):
        await message.channel.send(f"GoodMorning, {message.author.mention}!")
    elif content in ("hi", "hello"):
        await message.channel.send(f"Hello, {message.author.mention}!")

    # Anti-spam cooldown for leveling
    import time as _time

    now = _time.time()
    last = _last_counted.get(message.author.id, 0.0)
    if now - last < LEVEL_COOLDOWN_SECS:
        return
    _last_counted[message.author.id] = now

    total = await db.bump_message_count(message.author.id, str(message.author))
    for threshold, level in LEVEL_THRESHOLDS:
        if total == threshold:
            embed = discord.Embed(
                title="Level Up",
                description=f"Congratulations, {message.author}! You've reached Level {level}! 🎉",
                color=discord.Color.green(),
            )
            await message.channel.send(embed=embed)
            break


async def on_guild_join(guild):
    print("Bot joined")
    await db.set_prefix(guild.id, db.DEFAULT_PREFIX)

    channel = discord.utils.get(guild.text_channels)
    if channel is not None:
        embed = discord.Embed(
            title="Thank you for inviting me!",
            description="I'm here to assist you.",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/1108380972950491146/7349e4327248b681dcbfc171091aca07.png"
        )
        embed.add_field(
            name="Basic Commands", value="Here are some basic commands you can use:", inline=False
        )
        embed.add_field(
            name="!setprefix <new_prefix>", value="Change the bot's command prefix.", inline=False
        )
        embed.add_field(name="!ai <prompt>", value="Generate AI images.", inline=False)
        embed.add_field(name="!anicat", value="Display waifus.", inline=False)
        embed.add_field(
            name="!help", value="Display the full list of available commands.", inline=False
        )
        embed.set_footer(text="Powered by Catto0")
        await channel.send(embed=embed)
    else:
        print("The specified channel does not exist in the guild.")

    await _send_webhook(
        f"\n\n ------------------ **NEW BOT JOINED** ------------------ \n\n"
        f"**Guild Name**: `{guild.name}` \n"
        f"**Guild ID**: `{guild.id}` \n"
        f"**Member Count**: `{guild.member_count}`"
    )


async def on_guild_remove(guild):
    print("bot left")
    await db.delete_prefix(guild.id)
    await _send_webhook(
        f"\n\n ------------------ **BOT LEFT** ------------------ \n\n"
        f"**Guild Name**: `{guild.name}` \n"
        f"**Guild ID**: `{guild.id}` \n"
        f"**Member Count**: `{guild.member_count}`"
    )


async def _send_webhook(message: str) -> None:
    if not WEBHOOK_URL:
        return
    session = await get_session()
    webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)
    await webhook.send(message)


def setup(bot):
    bot.add_listener(on_guild_join)
    bot.add_listener(on_guild_remove)
    bot.add_listener(on_member_join)
    bot.add_listener(on_member_remove)
    bot.add_listener(on_message)
