#nitrix
import discord
from discord.ext import commands
import random
import requests


@commands.command(name="flip")
async def coin_flip(ctx, member: commands.MemberConverter = None):
    
    lists = ["Heads", "Tails"]
    result1 = random.choice(lists)

    if member:
        result2 = random.choice(lists)
        embed=discord.Embed(title="Coin Flip", description=f"You got {result1} and {member.mention} got {result2}",color=0x333333)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Coin Flip",description=f"You got {result1}",color=0x333333)
        await ctx.send(embed=embed)



