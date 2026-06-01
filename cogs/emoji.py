import contextlib

import discord
from discord.ext import commands

from core.logging import log_command

EMOJI_MAP = {
    "a": "🇦",
    "b": "🇧",
    "c": "🇨",
    "d": "🇩",
    "e": "🇪",
    "f": "🇫",
    "g": "🇬",
    "h": "🇭",
    "i": "🇮",
    "j": "🇯",
    "k": "🇰",
    "l": "🇱",
    "m": "🇲",
    "n": "🇳",
    "o": "🇴",
    "p": "🇵",
    "q": "🇶",
    "r": "🇷",
    "s": "🇸",
    "t": "🇹",
    "u": "🇺",
    "v": "🇻",
    "w": "🇼",
    "x": "🇽",
    "y": "🇾",
    "z": "🇿",
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
    " ": " ",
}


class Emoji(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="emojify", aliases=["e"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def emojify(self, ctx: commands.Context, *, msg: str):
        log_command(ctx)
        translated = " ".join(EMOJI_MAP[c] for c in msg.lower() if c in EMOJI_MAP)
        if not translated.strip():
            await ctx.send("Your message could not be emojified!")
            return
        with contextlib.suppress(discord.Forbidden, discord.NotFound):
            await ctx.message.delete()
        await ctx.send(translated)


async def setup(bot: commands.Bot):
    await bot.add_cog(Emoji(bot))
