import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command


class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="meme")
    async def meme(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get("https://meme-api.com/gimme") as resp:
                data = await resp.json()
            embed = discord.Embed(title=data["title"], url=data["postLink"])
            embed.set_image(url=data["url"])
            embed.set_footer(text=data["author"])
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        except Exception:
            await ctx.send("There was an error fetching a meme!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))
