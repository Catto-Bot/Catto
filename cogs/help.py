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
    "Gambler": "Economy",
    "Greet": "Welcome",
    "Moderation": "Moderation",
}

# Discord limits
MAX_FIELDS = 25
MAX_SELECT_OPTIONS = 25


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
        # Sort by command count desc, take top 24, group rest as Misc
        by_size = sorted(groups.items(), key=lambda kv: -len(kv[1]))
        top = by_size[: MAX_SELECT_OPTIONS - 1]
        rest = by_size[MAX_SELECT_OPTIONS - 1 :]
        self.misc: list[tuple[str, str]] = []
        for cog, cmds in rest:
            self.misc.extend(cmds)
        self.misc.sort()
        options = [
            discord.SelectOption(
                label=_display_name(cog)[:25],
                value=cog,
                emoji=COG_EMOJI.get(cog),
                description=f"{len(cmds)} commands"[:50],
            )
            for cog, cmds in top
        ]
        if self.misc:
            options.append(
                discord.SelectOption(
                    label="Other",
                    value="__misc__",
                    emoji="✨",
                    description=f"{len(self.misc)} commands",
                )
            )
        super().__init__(placeholder="Pick a category for details", options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.values[0]
        if cog == "__misc__":
            cmds = self.misc
            title = "✨ Other"
            color = discord.Color.greyple()
        else:
            cmds = self.groups[cog]
            title = f"{COG_EMOJI.get(cog, '•')} {_display_name(cog)}"
            color = discord.Color.blurple()
        embed = discord.Embed(title=title, color=color)
        for name, desc in cmds[:MAX_FIELDS]:
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
        lines: list[str] = []
        for cog in sorted(groups):
            emoji = COG_EMOJI.get(cog, "•")
            names = ", ".join(f"`/{n}`" for n, _ in groups[cog])
            if len(names) > 240:
                names = names[:237] + "..."
            lines.append(f"{emoji} **{_display_name(cog)}** ({len(groups[cog])}): {names}")
        description = (
            f"Server prefix: `{prefix}`. Slash variants also work.\n"
            f"Total commands: **{total}** across {len(groups)} categories.\n"
            f"Use `/help <command>` for details, or pick a category below.\n\n"
            + "\n".join(lines)
        )
        if len(description) > 4000:
            description = description[:3997] + "..."
        embed = discord.Embed(
            title="Catto Commands",
            description=description,
            color=discord.Color.blue(),
        )
        view = HelpView(ctx.author.id, groups, prefix)
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
