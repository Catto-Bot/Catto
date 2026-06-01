import contextlib
import json
import random
from pathlib import Path

import discord
from discord.ext import commands

from core import db
from core.logging import log_command
from core.views import Paginator

DATA_PATH = Path("data/data.json")
COOLDOWN = 60 * 60
PAGE_SIZE = 10
CLAIM_EMOJI = "<:anicat:1105722682160447550>"


class ClaimView(discord.ui.View):
    def __init__(self, card: dict, message: discord.Message | None = None):
        super().__init__(timeout=20.0)
        self.card = card
        self.claimed: discord.User | None = None
        self.message = message

    @discord.ui.button(label="Claim", emoji=CLAIM_EMOJI, style=discord.ButtonStyle.primary)
    async def claim(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        if self.claimed is not None:
            await interaction.response.send_message("Already claimed.", ephemeral=True)
            return
        self.claimed = interaction.user
        await db.record_anicat_claim(
            interaction.user.id,
            str(interaction.user),
            self.card["Name"],
            self.card["Points"],
        )
        embed = discord.Embed(title=f"Claimed by {interaction.user}")
        embed.set_image(url=self.card["Source"])
        embed.set_author(name=self.card["Name"])
        embed.set_footer(text="Thank you for using Catto Bot (AniCat)")
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    async def on_timeout(self) -> None:
        if self.claimed is not None or self.message is None:
            return
        embed = discord.Embed(title="Expired!", description="Nobody claimed in time.")
        embed.set_image(url=self.card["Source"])
        embed.set_footer(text="Thank you for using Catto Bot (AniCat)")
        for child in self.children:
            child.disabled = True
        with contextlib.suppress(discord.NotFound):
            await self.message.edit(embed=embed, view=self)


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
        embed = discord.Embed(title=card["Name"])
        embed.set_image(url=card["Source"])
        embed.set_footer(text=f"Points: {card['Points']}\nClick to claim")
        view = ClaimView(card)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg

    @commands.hybrid_command(name="anicatstats", aliases=["as", "stats"])
    async def anicatstats(self, ctx: commands.Context, member: discord.Member | None = None):
        log_command(ctx)
        target = member or ctx.author
        stats = await db.get_anicat_user(target.id)
        if not stats:
            await ctx.send("No record found.")
            return
        names = await db.list_anicat_claims(target.id)
        page_count = max(1, (len(names) + PAGE_SIZE - 1) // PAGE_SIZE)

        def render(page: int) -> discord.Embed:
            start, end = page * PAGE_SIZE, (page + 1) * PAGE_SIZE
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
            embed.set_footer(text=f"Page: {page + 1}/{page_count}")
            return embed

        view = Paginator(ctx.author.id, page_count, render)
        await ctx.send(embed=render(0), view=view)

    @commands.hybrid_command(name="anicatinfo", aliases=["aci"])
    async def anicatinfo(self, ctx: commands.Context, *, card: str):
        log_command(ctx)
        match = next((c for c in self.cards if card.lower() in c["Name"].lower()), None)
        if not match:
            await ctx.send("Not found")
            return
        embed = discord.Embed(title="MATCH FOUND!", description=match["Name"])
        embed.set_image(url=match["Source"])
        embed.set_footer(text="Thank you for using Catto Bot (AniCat)")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(AniCat(bot))
