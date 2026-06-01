import discord
from discord.ext import commands

from core import db
from core.logging import log_command

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
    "Help": "📖",
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
}


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx: commands.Context):
        log_command(ctx)
        prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else db.DEFAULT_PREFIX
        groups: dict[str, list[str]] = {}
        for cmd in self.bot.commands:
            if cmd.hidden or cmd.cog_name in (None, "Help"):
                continue
            groups.setdefault(cmd.cog_name, []).append(cmd.name)
        embed = discord.Embed(
            title="Catto Commands",
            description=f"Prefix for this server: `{prefix}` — slash variants also work.",
            color=discord.Color.blue(),
        )
        for cog_name in sorted(groups):
            emoji = COG_EMOJI.get(cog_name, "•")
            embed.add_field(
                name=f"{emoji} {cog_name}",
                value=", ".join(sorted(groups[cog_name])),
                inline=False,
            )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
