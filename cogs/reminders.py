import contextlib
import re
import time

import discord
from discord.ext import commands, tasks

from core import db
from core.logging import log_command

DURATION_RE = re.compile(r"^\s*(\d+)\s*(s|m|h|d)\s*$", re.IGNORECASE)
UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86_400}


def parse_duration(s: str) -> int | None:
    m = DURATION_RE.match(s)
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2).lower()
    return n * UNIT_SECONDS[unit]


class Reminders(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check.start()

    def cog_unload(self) -> None:
        self.check.cancel()

    @tasks.loop(seconds=30)
    async def check(self) -> None:
        now = int(time.time())
        for r in await db.due_reminders(now):
            channel = self.bot.get_channel(r["channel_id"])
            if channel is not None:
                with contextlib.suppress(discord.HTTPException):
                    await channel.send(f"<@{r['user_id']}> ⏰ {r['message']}")
            await db.delete_reminder(r["id"])

    @check.before_loop
    async def before_check(self) -> None:
        await self.bot.wait_until_ready()

    @commands.hybrid_command(name="remind", description="Set a reminder — duration like 30s, 5m, 2h, 1d")
    async def remind(self, ctx: commands.Context, duration: str, *, message: str):
        log_command(ctx)
        secs = parse_duration(duration)
        if secs is None:
            await ctx.send("Duration must look like `30m`, `2h`, `1d`.")
            return
        if secs < 10:
            await ctx.send("Minimum reminder is 10 seconds.")
            return
        if secs > 60 * 60 * 24 * 365:
            await ctx.send("Maximum reminder is 1 year.")
            return
        due = int(time.time()) + secs
        rid = await db.add_reminder(ctx.author.id, ctx.channel.id, due, message)
        ts = f"<t:{due}:R>"
        await ctx.send(f"Reminder #{rid} set for {ts}: {message}")

    @commands.hybrid_command(name="reminders", description="List your active reminders")
    async def reminders(self, ctx: commands.Context):
        log_command(ctx)
        items = await db.list_reminders(ctx.author.id)
        if not items:
            await ctx.send("You have no active reminders.")
            return
        lines = [f"#{r['id']} — <t:{r['due_at']}:R>: {r['message']}" for r in items]
        embed = discord.Embed(
            title=f"{ctx.author}'s reminders", description="\n".join(lines)
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="cancelreminder", description="Cancel one of your reminders by its ID")
    async def cancelreminder(self, ctx: commands.Context, reminder_id: int):
        log_command(ctx)
        items = await db.list_reminders(ctx.author.id)
        if not any(r["id"] == reminder_id for r in items):
            await ctx.send("No such reminder belongs to you.")
            return
        await db.delete_reminder(reminder_id)
        await ctx.send(f"Cancelled reminder #{reminder_id}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Reminders(bot))
