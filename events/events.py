import os

import discord
from dotenv import load_dotenv

from core import db
from core.http import get_session

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
        embed = discord.Embed(
            title=f"Welcome To Our Server {member}!",
            description="Make Sure To Read The Server Rules 🐱",
            color=discord.Color.dark_gray(),
        )
        embed.set_image(url="https://media.tenor.com/e976NPZxYp8AAAAd/peep-the-cat-rave-cat.gif")
        embed.set_thumbnail(
            url="https://w7.pngwing.com/pngs/885/246/png-transparent-cat-pusheen-desktop-animation-cute-stickers-mammal-animals-cat-like-mammal.png"
        )
        embed.set_footer(
            text="Thank You For Using Catto Bot 🐾",
            icon_url="https://i.pinimg.com/originals/57/39/74/573974c8b4f31d1c4ebda9aed0b46676.gif",
        )
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Error: {e}")


async def on_member_remove(member):
    try:
        channel_id = await db.get_leave_channel(member.guild.id)
        if channel_id is None:
            return
        channel = member.guild.get_channel(channel_id)
        if channel is None:
            return
        embed = discord.Embed(
            title=f"Sorry To See You Leave {member}!",
            description="Hope You Had A Great Time!",
            color=discord.Color.dark_gray(),
        )
        embed.set_thumbnail(
            url="https://w7.pngwing.com/pngs/885/246/png-transparent-cat-pusheen-desktop-animation-cute-stickers-mammal-animals-cat-like-mammal.gif"
        )
        embed.set_image(url="https://media.tenor.com/uICGiTPlUpgAAAAd/cat-leaving.png")
        embed.set_footer(
            text="Thank You For Using Catto Bot 🐾",
            icon_url="https://i.pinimg.com/originals/57/39/74/573974c8b4f31d1c4ebda9aed0b46676.gif",
        )
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Error: {e}")


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
