import discord
from discord.ext import commands

from core import db


class Greet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="setwelcomechannel")
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel(self, ctx: commands.Context, channel: discord.TextChannel):
        await db.set_welcome_channel(ctx.guild.id, channel.id)
        embed = discord.Embed(
            title="Success!", description=f"Welcome channel set to {channel.mention}"
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="deletewelcomechannel")
    @commands.has_permissions(administrator=True)
    async def deletewelcomechannel(self, ctx: commands.Context):
        await db.delete_welcome_channel(ctx.guild.id)
        embed = discord.Embed(title="Success!", description="Welcome channel cleared")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="setleavechannel")
    @commands.has_permissions(administrator=True)
    async def setleavechannel(self, ctx: commands.Context, channel: discord.TextChannel):
        await db.set_leave_channel(ctx.guild.id, channel.id)
        embed = discord.Embed(
            title="Success!", description=f"Leave channel set to {channel.mention}"
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="deleteleavechannel")
    @commands.has_permissions(administrator=True)
    async def deleteleavechannel(self, ctx: commands.Context):
        await db.delete_leave_channel(ctx.guild.id)
        embed = discord.Embed(title="Success!", description="Leave channel cleared")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Greet(bot))
