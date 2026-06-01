import discord
from discord.ext import commands

from core import db
from core.logging import log_command

COG_EMOJI: dict[str, str] = {
    "Coinflip": "🎲",
    "Dice": "🎲",
    "Meme": "🎭",
    "Anime": "🐱",
    "WouldYouRather": "❓",
    "Emoji": "✨",
    "Ship": "❤️",
    "Avatar": "🖼️",
    "FakeInfo": "🕵️",
    "Roles": "🔒",
    "Quotes": "📜",
    "Moderation": "🔨",
    "Hangman": "🎮",
    "Gifs": "🎥",
    "Chat": "💬",
    "AIImage": "🤖",
    "Gambler": "💰",
    "Tickets": "🎫",
    "Admin": "👨‍💻",
    "AniCat": "😼",
    "Valostats": "🎯",
    "Prefix": "⚙️",
    "Greet": "👋",
    "Confession": "🤫",
    "Profile": "👤",
    "Reminders": "⏰",
    "Polls": "📊",
    "Music": "🎵",
}

COG_DISPLAY: dict[str, str] = {
    "WouldYouRather": "Would You Rather",
    "AIImage": "AI Image",
    "AniCat": "AniCat",
    "FakeInfo": "Fake Info",
    "Valostats": "Valorant",
}


def _expand(cmd: commands.Command, prefix: str = "") -> list[tuple[str, str]]:
    """Flatten a command (and any subcommands) into [(name, description), ...]."""
    name = f"{prefix}{cmd.name}".strip()
    desc = cmd.description or cmd.help or ""
    if isinstance(cmd, commands.Group | commands.HybridGroup):
        out: list[tuple[str, str]] = [(name, desc)]
        for sub in sorted(cmd.commands, key=lambda c: c.name):
            out.extend(_expand(sub, f"{name} "))
        return out
    return [(name, desc)]


def _collect(bot: commands.Bot) -> dict[str, list[tuple[str, str]]]:
    """Group every visible command by cog name, expanding hybrid groups."""
    groups: dict[str, list[tuple[str, str]]] = {}
    for cmd in bot.commands:
        if cmd.hidden or cmd.cog_name in (None, "Help"):
            continue
        groups.setdefault(cmd.cog_name, []).extend(_expand(cmd))
    for k in groups:
        groups[k].sort()
    return groups


def _display_name(cog: str) -> str:
    return COG_DISPLAY.get(cog, cog)


class HelpSelect(discord.ui.Select):
    def __init__(self, groups: dict[str, list[tuple[str, str]]], prefix: str):
        self.groups = groups
        self.prefix = prefix
        options = [
            discord.SelectOption(
                label=_display_name(cog),
                value=cog,
                emoji=COG_EMOJI.get(cog),
                description=f"{len(cmds)} command(s)",
            )
            for cog, cmds in sorted(groups.items())
        ]
        super().__init__(placeholder="Pick a category for details", options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.values[0]
        embed = discord.Embed(
            title=f"{COG_EMOJI.get(cog, '•')} {_display_name(cog)}",
            color=discord.Color.blurple(),
        )
        for name, desc in self.groups[cog]:
            embed.add_field(name=f"/{name}", value=desc or "No description.", inline=False)
        embed.set_footer(text=f"Prefix: {self.prefix} . Pick another category below.")
        await interaction.response.edit_message(embed=embed, view=self.view)


class HelpView(discord.ui.View):
    def __init__(self, author_id: int, groups: dict[str, list[tuple[str, str]]], prefix: str):
        super().__init__(timeout=180)
        self.author_id = author_id
        self.add_item(HelpSelect(groups, prefix))

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
        groups = _collect(self.bot)

        if query:
            target = query.lstrip("/").lstrip(prefix).lower()
            for cog, cmds in groups.items():
                for name, desc in cmds:
                    if name.lower() == target:
                        embed = discord.Embed(
                            title=f"/{name}",
                            description=desc or "No description.",
                            color=discord.Color.blurple(),
                        )
                        embed.add_field(name="Category", value=_display_name(cog), inline=True)
                        await ctx.send(embed=embed)
                        return
            await ctx.send(f"No command matches `{query}`.")
            return

        total = sum(len(v) for v in groups.values())
        embed = discord.Embed(
            title="Catto Commands",
            description=(
                f"Server prefix: `{prefix}` . Slash variants also work.\n"
                f"Total commands: **{total}** across {len(groups)} categories.\n"
                f"Pick a category below to see details, or run `/help <command>`."
            ),
            color=discord.Color.blue(),
        )
        for cog in sorted(groups):
            names = ", ".join(f"`/{n}`" for n, _ in groups[cog])
            if len(names) > 256:
                names = names[:253] + "..."
            embed.add_field(
                name=f"{COG_EMOJI.get(cog, '•')} {_display_name(cog)}",
                value=names,
                inline=False,
            )
        view = HelpView(ctx.author.id, groups, prefix)
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
