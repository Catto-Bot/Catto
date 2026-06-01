import asyncio
import html

import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command


class Quotes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="quote")
    async def quote(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get("https://api.quotable.io/random") as resp:
                data = await resp.json()
            embed = discord.Embed(
                title=data["tags"][0] if data.get("tags") else "Quote",
                description=f"\"{data['content']}\"",
                color=0x777777,
            )
            embed.set_footer(text=f"-{data['author']}")
            msg = await ctx.channel.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        except Exception:
            await ctx.send("Error. Try Again!")

    @commands.hybrid_command(name="devjoke")
    async def devjoke(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get(
                "https://backend-omega-seven.vercel.app/api/getjoke"
            ) as resp:
                data = (await resp.json())[0]
            question, punchline = data["question"], data["punchline"]
            embed = discord.Embed(title=question, color=0x555555)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            embed = discord.Embed(title=f"{question}\n{punchline}", color=0x666666)
            await msg.edit(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        except Exception as err:
            await ctx.send(f"Couldn't fetch a dev joke: {err}")

    @commands.hybrid_command(name="dadjoke")
    async def dadjoke(self, ctx: commands.Context):
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
        except Exception:
            await ctx.send("My dad left me like your dad left to buy milk 😁")

    @commands.hybrid_command(name="trivia")
    async def trivia(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        async with session.get("https://opentdb.com/api.php?amount=1&type=boolean") as resp:
            data = (await resp.json())["results"][0]
        question = html.unescape(data["question"])
        correct = "🟩" if data["correct_answer"] == "True" else "❌"
        embed = discord.Embed(
            title=question,
            description=f"{data['category']} ({data['difficulty'].capitalize()})",
            color=0x333333,
        )
        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction("🟩")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return (
                user != ctx.bot.user
                and reaction.message.id == msg.id
                and str(reaction.emoji) in ["🟩", "❌"]
            )

        try:
            reaction, user = await ctx.bot.wait_for("reaction_add", timeout=20.0, check=check)
            verdict = (
                f"{user.mention} was right"
                if str(reaction.emoji) == correct
                else f"{user.mention} was wrong"
            )
            color = 0x00FF00 if str(reaction.emoji) == correct else 0xFF0000
            await ctx.send(embed=discord.Embed(description=verdict, color=color))
        except TimeoutError:
            await ctx.send(
                embed=discord.Embed(title="Nobody reacted on time 😔", color=0xFF0000)
            )

    @commands.hybrid_command(name="insult")
    async def insult(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get(
                "https://evilinsult.com/generate_insult.php?lang=en&type=json"
            ) as resp:
                data = await resp.json(content_type=None)
            embed = discord.Embed(title=html.unescape(data["insult"]), color=0x555555)
            await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(f"Couldn't fetch an insult: {err}")

    @commands.hybrid_command(name="darkmeme")
    async def darkmeme(self, ctx: commands.Context):
        log_command(ctx)
        await self._twopart_joke(ctx, "Dark", "💀")

    @commands.hybrid_command(name="spooky")
    async def spooky(self, ctx: commands.Context):
        log_command(ctx)
        await self._twopart_joke(ctx, "Spooky", "👍", "👎")

    async def _twopart_joke(self, ctx: commands.Context, category: str, *reactions: str):
        session = await get_session()
        try:
            async with session.get(
                f"https://v2.jokeapi.dev/joke/{category}?type=twopart"
            ) as resp:
                data = await resp.json()
            setup_text = html.unescape(data["setup"])
            delivery = html.unescape(data["delivery"])
            embed = discord.Embed(title=setup_text, color=0x555555)
            msg = await ctx.channel.send(embed=embed)
            await asyncio.sleep(3)
            embed = discord.Embed(title=f"{setup_text}\n{delivery}", color=0x666666)
            await msg.edit(embed=embed)
            for r in reactions:
                await msg.add_reaction(r)
        except Exception as err:
            await ctx.send(f"Couldn't fetch the joke: {err}")

    @commands.hybrid_command(name="advice")
    async def advice(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get("https://api.adviceslip.com/advice") as resp:
                data = await resp.json(content_type=None)
            embed = discord.Embed(title=html.unescape(data["slip"]["advice"]), color=0x555555)
            await ctx.channel.send(embed=embed)
        except Exception as err:
            await ctx.send(f"Couldn't fetch advice: {err}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Quotes(bot))
