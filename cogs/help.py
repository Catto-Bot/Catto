import discord
from discord.ext import commands

from core import db
from core.logging import log_command
from core.views import Paginator

# Friendly section emojis per cog name
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
}

FIELDS_PER_PAGE = 10


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="List every available command, grouped by feature")
    async def help(self, ctx: commands.Context):
        log_command(ctx)
        prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else db.DEFAULT_PREFIX
        groups: dict[str, list[str]] = {}
        for cmd in self.bot.commands:
            if cmd.hidden or cmd.cog_name in (None, "Help"):
                continue
            groups.setdefault(cmd.cog_name, []).append(cmd.name)
        ordered = sorted(groups.items())
        page_count = max(1, (len(ordered) + FIELDS_PER_PAGE - 1) // FIELDS_PER_PAGE)

        def render(page: int) -> discord.Embed:
            start, end = page * FIELDS_PER_PAGE, (page + 1) * FIELDS_PER_PAGE
            embed = discord.Embed(
                title="Catto Commands",
                description=f"Prefix for this server: `{prefix}` — slash variants also work.",
                color=discord.Color.blue(),
            )
            for cog_name, names in ordered[start:end]:
                emoji = COG_EMOJI.get(cog_name, "•")
                embed.add_field(
                    name=f"{emoji} {cog_name}",
                    value=", ".join(sorted(names)),
                    inline=False,
                )
            embed.set_footer(text=f"Page {page + 1}/{page_count}")
            return embed

        if page_count == 1:
            await ctx.send(embed=render(0))
            return
        view = Paginator(ctx.author.id, page_count, render)
        await ctx.send(embed=render(0), view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
