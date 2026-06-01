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

# (label, color, emoji, weight, points_range_inclusive)
RARITY_TIERS = [
    ("Common", 0x95A5A6, "⚪", 60, (0, 50)),
    ("Uncommon", 0x2ECC71, "🟢", 25, (51, 100)),
    ("Rare", 0x3498DB, "🔵", 10, (101, 150)),
    ("Epic", 0x9B59B6, "🟣", 4, (151, 200)),
    ("Legendary", 0xF1C40F, "🌟", 1, (201, 10_000)),
]


def _pick_rarity() -> tuple[str, int, str, tuple[int, int]]:
    total = sum(t[3] for t in RARITY_TIERS)
    roll = random.uniform(0, total)
    acc = 0.0
    for label, color, emoji, weight, rng in RARITY_TIERS:
        acc += weight
        if roll < acc:
            return label, color, emoji, rng
    label, color, emoji, _, rng = RARITY_TIERS[0]
    return label, color, emoji, rng


def _card_rarity_label(points: int) -> tuple[str, int, str]:
    for label, color, emoji, _, (lo, hi) in RARITY_TIERS:
        if lo <= points <= hi:
            return label, color, emoji
    return RARITY_TIERS[0][:3]


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
        label, color, emoji = _card_rarity_label(self.card["Points"])
        embed = discord.Embed(
            title=f"Claimed by {interaction.user}",
            description=f"{emoji} **{label}** card",
            color=color,
        )
        embed.set_image(url=self.card["Source"])
        embed.set_author(name=self.card["Name"])
        embed.set_footer(text=f"+{self.card['Points']} AniPoints")
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

    @commands.hybrid_group(name="anicat", aliases=["ac"], fallback="spawn", description="AniCat card game commands")
    @commands.cooldown(20, COOLDOWN, commands.BucketType.user)
    async def anicat(self, ctx: commands.Context):
        """Spawn a random anicat card. First to click the button claims it."""
        log_command(ctx)
        label, color, emoji, (lo, hi) = _pick_rarity()
        pool = [c for c in self.cards if lo <= c["Points"] <= hi]
        card = random.choice(pool or self.cards)
        embed = discord.Embed(
            title=f"{emoji} {card['Name']}",
            description=f"**{label}** card",
            color=color,
        )
        embed.set_image(url=card["Source"])
        embed.set_footer(text=f"Points: {card['Points']}  •  click below to claim")
        view = ClaimView(card)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg

    @anicat.command(name="stats", description="Show how many anicat cards a member has claimed")
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

    @anicat.command(name="info", description="Look up an anicat card by name")
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
