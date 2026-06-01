import discord
from discord.ext import commands

from core import db
from core.logging import log_command

# Map every cog into a clean user-facing meta-category.
# (meta name, emoji)
META: dict[str, tuple[str, str]] = {
    "Music": ("Music", "🎵"),
    "Gambler": ("Economy", "💰"),
    "AniCat": ("AniCat", "🐱"),
    "AIImage": ("AI", "🤖"),
    "Valostats": ("Valorant", "🎯"),
    "Moderation": ("Moderation", "🔨"),
    "Roles": ("Roles", "🔒"),
    "Tickets": ("Tickets", "🎫"),
    "Greet": ("Welcome", "👋"),
    "Prefix": ("Config", "⚙️"),
    "Profile": ("Profile", "👤"),
    "Reminders": ("Reminders", "⏰"),
    "Admin": ("Admin", "👨‍💻"),
    "Gifs": ("Social", "💞"),
    "Chat": ("Social", "💞"),
    "Confession": ("Social", "💞"),
    "Coinflip": ("Games", "🎮"),
    "Dice": ("Games", "🎮"),
    "WouldYouRather": ("Games", "🎮"),
    "Hangman": ("Games", "🎮"),
    "Polls": ("Games", "🎮"),
    "Ship": ("Games", "🎮"),
    "Meme": ("Fun", "🎭"),
    "Anime": ("Fun", "🎭"),
    "Quotes": ("Fun", "🎭"),
    "Emoji": ("Fun", "🎭"),
    "Avatar": ("Fun", "🎭"),
    "FakeInfo": ("Fun", "🎭"),
}

# Display order for the overview embed
META_ORDER = [
    "Music", "Economy", "Games", "Fun", "Social", "AniCat",
    "AI", "Valorant", "Moderation", "Roles", "Tickets",
    "Welcome", "Reminders", "Profile", "Config", "Admin",
]


def _expand(cmd: commands.Command, prefix: str = "") -> list[tuple[str, str]]:
    name = f"{prefix}{cmd.name}".strip()
    desc = cmd.description or cmd.help or ""
    if isinstance(cmd, commands.Group | commands.HybridGroup):
        out: list[tuple[str, str]] = [(name, desc)]
        for sub in sorted(cmd.commands, key=lambda c: c.name):
            out.extend(_expand(sub, f"{name} "))
        return out
    return [(name, desc)]


def _collect(bot: commands.Bot) -> dict[str, list[tuple[str, str]]]:
    """Return {meta_name: [(cmd_name, desc), ...]} grouped by META."""
    by_meta: dict[str, list[tuple[str, str]]] = {}
    for cmd in bot.commands:
        if cmd.hidden or cmd.cog_name in (None, "Help"):
            continue
        meta_name = META.get(cmd.cog_name, ("Other", "✨"))[0]
        by_meta.setdefault(meta_name, []).extend(_expand(cmd))
    for k in by_meta:
        by_meta[k].sort()
    return by_meta


def _meta_emoji(meta: str) -> str:
    for _, (m, e) in META.items():
        if m == meta:
            return e
    return "✨"


class HelpSelect(discord.ui.Select):
    def __init__(self, by_meta: dict[str, list[tuple[str, str]]], prefix: str):
        self.by_meta = by_meta
        self.prefix = prefix
        options = [
            discord.SelectOption(
                label=meta,
                value=meta,
                emoji=_meta_emoji(meta),
                description=f"{len(by_meta[meta])} commands",
            )
            for meta in META_ORDER
            if meta in by_meta
        ][:25]
        super().__init__(placeholder="Pick a category to see commands", options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        meta = self.values[0]
        cmds = self.by_meta[meta]
        embed = discord.Embed(
            title=f"{_meta_emoji(meta)}  {meta}",
            description=f"{len(cmds)} command(s)",
            color=discord.Color.blurple(),
        )
        for name, desc in cmds[:25]:
            embed.add_field(name=f"/{name}", value=desc or "\u200b", inline=False)
        embed.set_footer(text=f"Prefix: {self.prefix}  .  /help <command> for details")
        await interaction.response.edit_message(embed=embed, view=self.view)


class HelpView(discord.ui.View):
    def __init__(self, author_id: int, by_meta: dict[str, list[tuple[str, str]]], prefix: str):
        super().__init__(timeout=180)
        self.author_id = author_id
        self.add_item(HelpSelect(by_meta, prefix))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Only the command author can navigate this menu.", ephemeral=True
            )
            return False
        return True


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Show every command, grouped by feature")
    async def help(self, ctx: commands.Context, *, query: str | None = None):
        log_command(ctx)
        prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else db.DEFAULT_PREFIX
        by_meta = _collect(self.bot)

        # Single-command lookup
        if query:
            target = query.lstrip("/").lstrip(prefix).lower()
            for meta, cmds in by_meta.items():
                for name, desc in cmds:
                    if name.lower() == target:
                        embed = discord.Embed(
                            title=f"/{name}",
                            description=desc or "No description.",
                            color=discord.Color.blurple(),
                        )
                        embed.add_field(name="Category", value=meta, inline=True)
                        await ctx.send(embed=embed)
                        return
            await ctx.send(f"No command matches `{query}`.")
            return

        total = sum(len(v) for v in by_meta.values())
        embed = discord.Embed(
            title="Catto",
            description=(
                f"A multipurpose Discord bot. **{total} commands** across "
                f"**{len(by_meta)} categories**.\n"
                f"Server prefix: `{prefix}`.  Use `/help <command>` for details.\n"
                f"Pick a category below to explore."
            ),
            color=discord.Color.from_rgb(88, 101, 242),
        )
        # Render as a 3-column grid via inline fields, max 24 to be safe
        for meta in META_ORDER:
            if meta not in by_meta:
                continue
            count = len(by_meta[meta])
            preview = ", ".join(f"`{n.split()[-1]}`" for n, _ in by_meta[meta][:4])
            if count > 4:
                preview += f", +{count - 4}"
            embed.add_field(
                name=f"{_meta_emoji(meta)} {meta}  ({count})",
                value=preview or "\u200b",
                inline=True,
            )
        embed.set_footer(text="Tip: use the dropdown for full command details")
        view = HelpView(ctx.author.id, by_meta, prefix)
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
