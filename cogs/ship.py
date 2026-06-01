import random

import discord
from discord.ext import commands

from core.logging import log_command


class Ship(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ship")
    async def ship(self, ctx: commands.Context, member: discord.Member):
        log_command(ctx)
        percent = random.randint(0, 100)
        embed = discord.Embed(title="❤️ **MATCHMAKING** ❤️", color=0xFF69B4)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name=ctx.author.display_name, value="🔻", inline=True)
        embed.add_field(name="💖💖", value=f"{percent}%", inline=True)
        embed.add_field(name=member.display_name, value="🔻", inline=True)
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ship(bot))
