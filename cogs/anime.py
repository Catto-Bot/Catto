import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command


class Anime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="animeQuote")
    async def anime_quote(self, ctx: commands.Context):
        log_command(ctx)
        loading = await ctx.send("loading…")
        session = await get_session()
        try:
            async with session.get("https://animechan.vercel.app/api/random") as resp:
                data = await resp.json()
            embed = discord.Embed(
                title=f"Anime Name: {data['anime']}",
                description=f"'{data['quote']}'",
                color=0x555555,
            )
            embed.set_footer(text=f"-{data['character']}")
            await loading.delete()
            await ctx.send(embed=embed)
        except Exception:
            await loading.delete()
            await ctx.send("TATAKAE! 🕊️ - Eren Yeager")

    @commands.hybrid_command(name="something")
    async def something(self, ctx: commands.Context):
        log_command(ctx)
        embed = discord.Embed(
            title="⏲ This feature is work in progress!",
            description="It will soon be available!",
            color=0x89CFF0,
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Anime(bot))
