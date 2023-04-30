#kadota
import discord
from discord.ext import commands
import random


@commands.command(name="rolldice")
async def rolldice(ctx, member: commands.MemberConverter = None):
    dice_roll = random.randint(1,6)
    
    if member:
        dice_roll2 = random.randint(1,6)
        await ctx.channel.send(f"{ctx.author.name} rolled a {dice_roll}! and {member.name}! rolled a {dice_roll2}")
        if dice_roll>dice_roll2:
            await ctx.channel.send(f"{ctx.author.name} WON!!!")
        
        elif dice_roll2>dice_roll:
            await ctx.channel.send(f"{member.name} WON!!!")
        else:
            await ctx.channel.send("draw")
    else:
        await ctx.channel.send(f"You rolled {dice_roll}")

