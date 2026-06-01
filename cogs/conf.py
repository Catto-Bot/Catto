from datetime import datetime

import discord
from discord.ext import commands

from core import db


class Confession(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="confessionsetup")
    @commands.has_permissions(administrator=True)
    async def confessionsetup(self, ctx: commands.Context, channel: discord.TextChannel):
        await db.set_confession_channel(ctx.guild.id, channel.id)
        await ctx.send(f"Confession channel set to {channel.mention}")

    @commands.hybrid_command(name="ch")
    async def ch(self, ctx: commands.Context, *, message: str):
        configured = await db.get_confession_channel(ctx.guild.id)
        if configured != ctx.channel.id:
            return
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass
        prefix = await db.get_prefix(ctx.guild.id)
        embed = discord.Embed(
            description=message,
            color=discord.Color.green(),
            timestamp=datetime.now(),
        )
        embed.set_footer(text=f"{prefix}ch (message)")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Confession(bot))
