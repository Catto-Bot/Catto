import datetime

import discord
from discord.ext import commands

from core import db
from core.logging import log_command


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx: commands.Context):
        log_command(ctx)
        prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else db.DEFAULT_PREFIX
        embed = discord.Embed(
            title="Catto Commands",
            description="Here are the available commands:",
            color=discord.Color.blue(),
        )
        embed.add_field(name="👨‍💻 Main", value="info, ai, uptime", inline=False)
        embed.add_field(name="😼 AniCat", value="anicat, anicatstats, anicatinfo", inline=False)
        embed.add_field(
            name="💰 CattoGamble",
            value="monie, balance, daily, weekly, bet, steal, leaderboard, give",
            inline=False,
        )
        embed.add_field(name="🎮 ValoStats", value="vstats, valofight", inline=False)
        embed.add_field(name="💬 Chat", value="chat, learn", inline=False)
        embed.add_field(name="🐱 Anime", value="animequote", inline=False)
        embed.add_field(name="🖼️ Avatar", value="avatar", inline=False)
        embed.add_field(name="✨ Emojify", value="emojify", inline=False)
        embed.add_field(
            name="🎥 Gifs",
            value="hug, slap, kiss, lick, bite, bully, blush, cry, cuddle, smug, bonk, pat, handhold, nom, kill, wink, poke",
            inline=False,
        )
        embed.add_field(
            name="👋 Greet",
            value="setwelcomechannel, setleavechannel, deletewelcomechannel, deleteleavechannel",
            inline=False,
        )
        embed.add_field(
            name="🎭 Meme", value="meme, darkmeme, dadjoke, devjoke, bored", inline=False
        )
        embed.add_field(name="🎮 Games", value="trivia, hangman", inline=False)
        embed.add_field(name="🔨 Moderation", value="mute, kick, ban, unmute", inline=False)
        embed.add_field(name="⚙️ Prefix", value="prefix, setprefix", inline=False)
        embed.add_field(name="📜 Quotes", value="quote, insult, spooky, advice", inline=False)
        embed.add_field(
            name="🔒 Roles",
            value="setuprole, createrole, removerole, deleterole",
            inline=False,
        )
        embed.add_field(name="🎫 Ticket", value="ticketsetup, deleteticket", inline=False)
        embed.add_field(name="❓ Would You Rather?", value="wyr, truth, dare", inline=False)
        embed.add_field(
            name="🎲 Other",
            value="flip, rps, announce, cat, rolldice, ship, catfact, fakeinfo",
            inline=False,
        )
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embed.set_footer(text=f"Prefix for this server: {prefix} | Generated at: {now}")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
