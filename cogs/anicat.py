import json
import random
import time
from pathlib import Path

import discord
from discord.ext import commands

from core import db
from core.logging import log_command

DATA_PATH = Path("data/data.json")
COOLDOWN = 60 * 60
PAGE_SIZE = 10


class AniCat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with DATA_PATH.open(encoding="utf8") as f:
            self.cards = json.load(f)

    @commands.hybrid_command(name="anicat", aliases=["ac", "anic"])
    @commands.cooldown(20, COOLDOWN, commands.BucketType.user)
    async def anicat(self, ctx: commands.Context):
        log_command(ctx)
        card = random.choice(self.cards)
        embed = discord.Embed(title=card["Name"], description="")
        embed.set_image(url=card["Source"])
        embed.set_footer(text=f"Points: {card['Points']}\nReact to claim")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("<:anicat:1105722682160447550>")

        def check(reaction, user):
            return (
                reaction.message.id == msg.id
                and user != ctx.bot.user
                and str(reaction.emoji) == "<:anicat:1105722682160447550>"
            )

        try:
            _, user = await ctx.bot.wait_for("reaction_add", timeout=20.0, check=check)
        except TimeoutError:
            expired = discord.Embed(
                title="Expired!", description="Nobody claimed in time."
            )
            expired.set_image(url=card["Source"])
            expired.set_footer(text="Thank you for using Catto Bot (AniCat)")
            await msg.clear_reactions()
            await msg.edit(embed=expired)
            return

        await db.record_anicat_claim(user.id, str(user), card["Name"], card["Points"])
        claimed = discord.Embed(title=f"Claimed by {user}", description="")
        claimed.set_image(url=card["Source"])
        claimed.set_author(name=card["Name"])
        claimed.set_footer(text="Thank you for using Catto Bot (AniCat)")
        await msg.clear_reactions()
        await msg.edit(embed=claimed)

    @commands.hybrid_command(name="anicatstats", aliases=["as", "stats"])
    async def anicatstats(self, ctx: commands.Context, member: discord.Member | None = None):
        log_command(ctx)
        target = member or ctx.author
        stats = await db.get_anicat_user(target.id)
        if not stats:
            await ctx.send("No record found.")
            return
        names = await db.list_anicat_claims(target.id)

        page = 0

        def build_embed(p: int):
            start, end = p * PAGE_SIZE, (p + 1) * PAGE_SIZE
            embed = discord.Embed(
                title=f"AniCat Info for {stats['username']}", color=discord.Color.magenta()
            )
            embed.add_field(name="Total Anicats", value=stats["total_cats"], inline=False)
            embed.add_field(name="Total AniPoints", value=stats["total_pts"], inline=False)
            embed.add_field(
                name="Anicats Info",
                value="\n".join(names[start:end]) or "(none)",
                inline=False,
            )
            embed.set_footer(text=f"Page: {p + 1}/{max(1, (len(names) + PAGE_SIZE - 1) // PAGE_SIZE)}")
            return embed

        msg = await ctx.send(embed=build_embed(page))
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == msg.id
                and str(reaction.emoji) in ["⬅️", "➡️"]
            )

        end_time = time.time() + 60
        while time.time() < end_time:
            try:
                reaction, user = await ctx.bot.wait_for(
                    "reaction_add", timeout=end_time - time.time(), check=check
                )
            except TimeoutError:
                break
            if str(reaction.emoji) == "➡️" and (page + 1) * PAGE_SIZE < len(names):
                page += 1
            elif str(reaction.emoji) == "⬅️" and page > 0:
                page -= 1
            await msg.edit(embed=build_embed(page))
            try:
                await msg.remove_reaction(reaction, user)
            except (discord.Forbidden, discord.NotFound):
                pass

    @commands.hybrid_command(name="anicatinfo", aliases=["aci"])
    async def anicatinfo(self, ctx: commands.Context, *, card: str):
        log_command(ctx)
        match = next(
            (c for c in self.cards if card.lower() in c["Name"].lower()), None
        )
        if not match:
            await ctx.send("Not found")
            return
        embed = discord.Embed(title="MATCH FOUND!", description=match["Name"])
        embed.set_image(url=match["Source"])
        embed.set_footer(text="Thank you for using Catto Bot (AniCat)")
        await ctx.send(embed=embed)

    @anicat.error
    async def anicat_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes = round(error.retry_after / 60)
            embed = discord.Embed(
                title="This command is on cooldown!",
                description=f"Try again in {minutes} minute(s)",
            )
            await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(AniCat(bot))
