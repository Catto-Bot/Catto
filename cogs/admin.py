import os
import time

import discord
import psutil
from discord.ext import commands

from core import db
from core.http import get_session
from core.logging import log_command

OWNER_IDS = {
    int(uid) for uid in os.getenv("OWNER_IDS", "").split(",") if uid.strip()
}
PRIMARY_OWNER_ID = int(os.getenv("PRIMARY_OWNER_ID", "0") or 0)


def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNER_IDS
    return commands.check(predicate)


def is_primary_owner():
    async def predicate(ctx):
        return PRIMARY_OWNER_ID and ctx.author.id == PRIMARY_OWNER_ID
    return commands.check(predicate)


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context):
        log_command(ctx)
        start = time.time()
        msg = await ctx.send("Pinging…")
        session = await get_session()
        async with session.get("https://icanhazdadjoke.com/slack"):
            pass
        latency = (time.time() - start) * 1000
        bot_latency = ctx.bot.latency * 1000
        embed = discord.Embed(title="Bot Latency")
        embed.add_field(name="API roundtrip", value=f"{latency:.2f} ms", inline=False)
        embed.add_field(name="Gateway", value=f"{bot_latency:.2f} ms", inline=False)
        await msg.delete()
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="info")
    async def info(self, ctx: commands.Context):
        log_command(ctx)
        devs = ["Ghost Riley#6077", "Nitrix#1271", "kadota#1408", "aryn#5511"]
        embed = discord.Embed(
            title="Developers", description="\n".join(devs), color=0x000000
        )
        embed.add_field(name="Bot Version", value="2.0", inline=False)
        embed.add_field(name="Coded in", value="`discord.py`", inline=False)
        embed.add_field(
            name="GitHub", value="`https://github.com/Catto-Bot/Catto`", inline=False
        )
        embed.add_field(
            name="Support", value="`https://discord.gg/cvNa9XTbD9`", inline=False
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="invite")
    async def invite(self, ctx: commands.Context):
        log_command(ctx)
        embed = discord.Embed(
            title="Invite Catto",
            description="https://discord.com/oauth2/authorize?client_id=1108380972950491146&permissions=8&scope=bot",
        )
        embed.set_footer(text="Thank you for using Catto!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        log_command(ctx)
        elapsed = time.time() - self.start_time
        weeks, elapsed = divmod(elapsed, 604_800)
        days, elapsed = divmod(elapsed, 86_400)
        hours, elapsed = divmod(elapsed, 3600)
        minutes, seconds = divmod(elapsed, 60)
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        out = (
            f"{int(weeks)}w {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s\n"
            f"CPU: {cpu}%, Memory: {mem}%, Disk: {disk}%"
        )
        await ctx.send(f"```{out}```")

    @commands.hybrid_command(name="vote")
    async def vote(self, ctx: commands.Context):
        log_command(ctx)
        embed = discord.Embed(
            title="Vote for the Bot!",
            description="Click [here](https://top.gg/bot/1108380972950491146/invite) to vote for the bot!",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="servers")
    @is_owner()
    async def servers(self, ctx: commands.Context):
        log_command(ctx)
        lines = []
        total_members = 0
        for i, guild in enumerate(ctx.bot.guilds):
            lines.append(f"#{i}, {guild}, {guild.member_count}, id = {guild.id}")
            total_members += guild.member_count
        out = "\n".join(lines)
        await ctx.send(
            f"Server info for {ctx.bot.user.name} ({len(ctx.bot.guilds)} servers, {total_members} members)",
            file=discord.File(__import__("io").BytesIO(out.encode()), filename="servers.txt"),
        )

    @commands.hybrid_command(name="addai")
    @is_primary_owner()
    async def addai(self, ctx: commands.Context, user_id: str):
        log_command(ctx)
        if not user_id.isdigit():
            await ctx.send("Provide a numeric user ID.")
            return
        await db.add_ai_allowed(int(user_id))
        await ctx.send("done")

    @commands.command(name="sync")
    @is_owner()
    async def sync(self, ctx: commands.Context, scope: str = "guild"):
        """Sync slash commands. scope=guild (default, instant) or global (slow)."""
        log_command(ctx)
        if scope == "global":
            synced = await ctx.bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} commands globally (may take up to 1h to appear).")
            return
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} commands to this guild.")

    @servers.error
    async def servers_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("This command is restricted to bot owners.")

    @addai.error
    async def addai_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("This command is restricted to the primary owner.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
