import random

import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command
from core.views import ConfirmView


class Coinflip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="flip", description="Flip a coin (mention a user to flip against them)")
    async def flip(self, ctx: commands.Context, member: discord.Member | None = None):
        log_command(ctx)
        result1 = random.choice(["Heads", "Tails"])
        if member:
            result2 = random.choice(["Heads", "Tails"])
            embed = discord.Embed(
                title="Coin Flip",
                description=f"You got {result1} and {member.mention} got {result2}",
                color=0x333333,
            )
        else:
            embed = discord.Embed(
                title="Coin Flip", description=f"You got {result1}", color=0x333333
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="rps", description="Play rock-paper-scissors against the bot")
    async def rps(self, ctx: commands.Context, choice: str | None = None):
        log_command(ctx)
        options = ["rock", "paper", "scissors"]
        if not choice or choice.lower() not in options:
            embed = discord.Embed(
                title="Correct Syntax:",
                description="!rps <choice> (rock, paper, scissors)",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return
        user_choice = choice.lower()
        bot_choice = random.choice(options)
        if user_choice == bot_choice:
            result = "It's a draw. Try again"
        elif (
            (user_choice == "rock" and bot_choice == "scissors")
            or (user_choice == "paper" and bot_choice == "rock")
            or (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = "You Win 🏆"
        else:
            result = "You lose 😢"
        embed = discord.Embed(
            title="Rock Paper Scissors",
            description=f"The bot chose {bot_choice}. {result}",
            color=0x555555,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="announce", aliases=["announcement"], description="Post an announcement (asks whether to embed)")
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx: commands.Context, *, message: str):
        log_command(ctx)
        view = ConfirmView(ctx.author.id)
        prompt = await ctx.send("Embed this announcement?", view=view)
        await view.wait()
        await prompt.delete()
        if view.value is True:
            embed = discord.Embed(
                title="Announcement 🔊", description=message, color=0x333333
            )
            await ctx.send(embed=embed)
        elif view.value is False:
            await ctx.send(message)

    @commands.hybrid_command(name="joke", aliases=["jokes"], description="Get a random dad joke")
    async def joke(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get(
                "https://icanhazdadjoke.com/slack",
                headers={"Accept": "application/json"},
            ) as resp:
                data = await resp.json()
            text = data["attachments"][0]["fallback"]
            embed = discord.Embed(title=text, color=0x555555)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        except Exception as err:
            await ctx.send(f"Could not fetch a joke: {err}")

    @commands.hybrid_command(name="catfact", aliases=["cfact", "catfacts"], description="Get a random cat fact")
    async def catfact(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get("https://catfact.ninja/fact") as resp:
                data = await resp.json()
            embed = discord.Embed(title=data["fact"], color=0x555555)
            await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(f"Could not fetch a cat fact: {err}")

    @commands.hybrid_command(name="bored", description="Suggest an activity when you're bored")
    async def bored(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get("https://www.boredapi.com/api/activity") as resp:
                data = await resp.json()
            embed = discord.Embed(title=f"{data['activity']}.", color=0x555555)
            await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(f"Could not fetch an activity: {err}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Coinflip(bot))
