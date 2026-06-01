import discord
from discord.ext import commands

from core import db


class Greet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="welcome", description="Welcome/leave channel configuration")
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx: commands.Context):
        await ctx.send("Subcommands: setjoin, clearjoin, setleave, clearleave")

    @welcome.command(name="setjoin", description="Set the channel where new members are welcomed")
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel(self, ctx: commands.Context, channel: discord.TextChannel):
        await db.set_welcome_channel(ctx.guild.id, channel.id)
        embed = discord.Embed(
            title="Success!", description=f"Welcome channel set to {channel.mention}"
        )
        await ctx.send(embed=embed)

    @welcome.command(name="clearjoin", description="Stop sending welcome messages in this server")
    @commands.has_permissions(administrator=True)
    async def deletewelcomechannel(self, ctx: commands.Context):
        await db.delete_welcome_channel(ctx.guild.id)
        embed = discord.Embed(title="Success!", description="Welcome channel cleared")
        await ctx.send(embed=embed)

    @welcome.command(name="setleave", description="Set the channel where member-leave messages are posted")
    @commands.has_permissions(administrator=True)
    async def setleavechannel(self, ctx: commands.Context, channel: discord.TextChannel):
        await db.set_leave_channel(ctx.guild.id, channel.id)
        embed = discord.Embed(
            title="Success!", description=f"Leave channel set to {channel.mention}"
        )
        await ctx.send(embed=embed)

    @welcome.command(name="clearleave", description="Stop sending leave messages in this server")
    @commands.has_permissions(administrator=True)
    async def deleteleavechannel(self, ctx: commands.Context):
        await db.delete_leave_channel(ctx.guild.id)
        embed = discord.Embed(title="Success!", description="Leave channel cleared")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Greet(bot))
