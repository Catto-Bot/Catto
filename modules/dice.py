#kadota
import discord
from discord.ext import commands
import random


@commands.command(name="rolldice")
async def rolldice(ctx):
    dice_roll = random.randint(1,6)
    await ctx.channel.send(f" bahahaha You rolled a {dice_roll}")

