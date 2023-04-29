#nitrix
import discord
from discord.ext import commands
import random
import requests

# @commands.command(name="flip")
# async def coin_flip(ctx):  
#     list=["Heads","Tails"]
#     result = random.choice(list)
#     await ctx.channel.send(f" You got {result}")



# @commands.command(name="flip")
# async def coin_flip(ctx,member:commands.MemberConverter):  
#     list=["Heads","Tails"]
#     result1 = random.choice(list)
#     result2 = random.choice(list)
#     await ctx.channel.send(f" You got {result1} and {member.mention} got {result2}")



@commands.command(name="flip")
async def coin_flip(ctx, member: commands.MemberConverter = None):
    list = ["Heads", "Tails"]
    result1 = random.choice(list)
    if member:
        result2 = random.choice(list)
        await ctx.channel.send(f"You got {result1} and {member.mention} got {result2}")
    else:
        await ctx.channel.send(f"You got {result1}")
