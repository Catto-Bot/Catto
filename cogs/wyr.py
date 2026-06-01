import re

import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command


class WouldYouRather(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="wyr")
    async def wyr(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get("https://api.truthordarebot.xyz/api/wyr") as resp:
                data = await resp.json()
            question = data["question"]
        except Exception as err:
            await ctx.send(f"Could not fetch a question: {err}")
            return

        options = re.findall(r"rather\s(.*?)\sor\s(.*?)\?", question, re.IGNORECASE)
        if not options:
            await ctx.send(question)
            return
        option1, option2 = options[0]

        embed = discord.Embed(title="WOULD YOU RATHER?", color=0x333333)
        embed.add_field(name="Would you rather", value=option1, inline=True)
        embed.add_field(name="Or", value=option2, inline=True)
        message = await ctx.send(embed=embed)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        voted: set[int] = set()
        vote_count = {option1: 0, option2: 0}

        def check(reaction, user):
            return (
                reaction.message.id == message.id
                and user != ctx.bot.user
                and str(reaction.emoji) in ["⬅️", "➡️"]
                and user.id not in voted
            )

        try:
            while True:
                reaction, user = await ctx.bot.wait_for(
                    "reaction_add", check=check, timeout=30
                )
                await message.remove_reaction(reaction, user)
                voted.add(user.id)
                if str(reaction.emoji) == "⬅️":
                    vote_count[option1] += 1
                else:
                    vote_count[option2] += 1
                embed.clear_fields()
                embed.add_field(
                    name="Would you rather",
                    value=f"{option1}\nVotes: {vote_count[option1]}",
                    inline=True,
                )
                embed.add_field(
                    name="Or",
                    value=f"{option2}\nVotes: {vote_count[option2]}",
                    inline=True,
                )
                await message.edit(embed=embed)
        except TimeoutError:
            embed.title = "time limit reached"
            await message.clear_reactions()
            await message.edit(embed=embed)

    @commands.hybrid_command(name="truth")
    async def truth(self, ctx: commands.Context):
        log_command(ctx)
        await self._fetch(ctx, "https://api.truthordarebot.xyz/api/truth")

    @commands.hybrid_command(name="dare")
    async def dare(self, ctx: commands.Context):
        log_command(ctx)
        await self._fetch(ctx, "https://api.truthordarebot.xyz/api/dare")

    async def _fetch(self, ctx: commands.Context, url: str):
        msg = await ctx.send("``Fetching..``")
        session = await get_session()
        try:
            async with session.get(url) as resp:
                data = await resp.json()
            await msg.edit(content=f"```{data['question']}```")
        except Exception as err:
            await msg.delete()
            await ctx.send(f"``{err}``")


async def setup(bot: commands.Bot):
    await bot.add_cog(WouldYouRather(bot))
