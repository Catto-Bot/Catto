import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from core.http import get_session
from core.logging import log_command

load_dotenv()
CAT_API_KEY = os.getenv("CAT_API_KEY")

DICE_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Dice-1-b.svg/1024px-Dice-1-b.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Dice-2-b.svg/1200px-Dice-2-b.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Dice-3-b.svg/1200px-Dice-3-b.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Dice-4-b.svg/557px-Dice-4-b.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Dice-5-b.svg/2048px-Dice-5-b.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Dice-6-b.svg/768px-Dice-6-b.svg.png",
]


class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="rolldice")
    async def rolldice(self, ctx: commands.Context, member: discord.Member | None = None):
        log_command(ctx)
        roll = random.randint(1, 6)
        img = DICE_IMAGES[roll - 1]
        if member:
            roll2 = random.randint(1, 6)
            outcome = f"{ctx.author.name} rolled a {roll}! and {member.name} rolled a {roll2}!"
            embed = discord.Embed(
                title=f"{ctx.author.name}\tVS\t{member.name}",
                description=outcome,
                color=0x333333,
            )
            if roll > roll2:
                embed.set_footer(text=f"Winner: {ctx.author.name} 🏆")
            elif roll2 > roll:
                embed.set_footer(text=f"Winner: {member.name} 🏆")
            else:
                embed.set_footer(text="DRAW!!!")
            embed.set_thumbnail(url=img)
        else:
            embed = discord.Embed(
                title="DICE ROLL RESULTS",
                description=f"You rolled a {roll}!",
                color=0x333333,
            )
            embed.set_thumbnail(url=img)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="cat")
    async def cat(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search",
                headers={"x-api-key": CAT_API_KEY} if CAT_API_KEY else {},
            ) as resp:
                data = await resp.json()
            await ctx.send(data[0]["url"])
        except Exception:
            await ctx.send("Can't find cute cat image :(")


async def setup(bot: commands.Bot):
    await bot.add_cog(Dice(bot))
