import datetime

import discord
from discord.ext import commands

from core.logging import log_command


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="mod", description="Moderation commands")
    @commands.has_permissions(moderate_members=True)
    async def mod(self, ctx: commands.Context):
        await ctx.send("Subcommands: mute, unmute, kick, ban")

    @mod.command(name="mute", description="Timeout a member for N minutes")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx: commands.Context, user: discord.Member, minutes: int):
        log_command(ctx)
        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await user.timeout(until, reason=f"muted for {minutes} minute(s)")
        await ctx.send(f"{user.mention} has been muted for {minutes} minute(s)")

    @mod.command(name="unmute", description="Remove a member's timeout")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx: commands.Context, user: discord.Member):
        log_command(ctx)
        if user.timed_out_until is None:
            await ctx.send(f"{user.mention} is not muted.")
            return
        await user.timeout(None, reason="unmuted")
        await ctx.send(f"{user.mention} has been unmuted")

    @mod.command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member):
        log_command(ctx)
        await user.kick()
        await ctx.send(f"The user ({user}) has been kicked out of the server")

    @mod.command(name="ban", description="Ban a member from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member):
        log_command(ctx)
        await user.ban()
        await ctx.send(f"The user ({user}) has been banned")


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
