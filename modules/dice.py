#kadota
import discord
from discord.ext import commands
import random


@commands.command(name="rolldice")
async def rolldice(ctx, member: commands.MemberConverter = None):
    dice_roll = random.randint(1,6)
    
    if member:
        dice_roll2 = random.randint(1,6)
        outcome_msg = f"{ctx.author.name} rolled a {dice_roll}! and {member.name} rolled a {dice_roll2}!"
        if dice_roll > dice_roll2:
            outcome_msg += f" \n{ctx.author.name} WON!!!"
        elif dice_roll2 > dice_roll:
            outcome_msg += f" \n{member.name} WON!!!"
        else:
            outcome_msg += " \nDRAW!!"
        await ctx.channel.send(outcome_msg)
    else:
        await ctx.channel.send(f"You rolled {dice_roll}!")

