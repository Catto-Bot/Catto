import discord
from discord.ext import commands

from core import db


class Prefix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="setprefix")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context, prefix: str):
        await db.set_prefix(ctx.guild.id, prefix)
        await ctx.send(f"Prefix changed to: {prefix}")

    @commands.hybrid_command(name="prefix")
    async def prefix(self, ctx: commands.Context):
        p = await db.get_prefix(ctx.guild.id)
        embed = discord.Embed(title="Prefix", description=f"The prefix for this server is `{p}`")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Prefix(bot))
