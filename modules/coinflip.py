#nitrix
from discord.ext import commands
import random

@commands.command(name="roll_dice")
async def roll_dice(ctx):
    """
    Roll a six-sided die and display the result.
    """
    result = random.randint(1, 6)
    await ctx.channel.send(f"The result is {result}!")
