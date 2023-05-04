#nitrix
import discord
from discord.ext import commands
import random
import requests

#COINFLIP

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


#RPS

@commands.command(name="rps")
async def rps_game(ctx,user_choice):

    list=["rock","paper","scissors"]
    bot_choice=random.choice(list)

    user_choice=user_choice.lower()

    if (user_choice not in list):
        await ctx.send("Please type rock, paper or scissors")

    
    if(user_choice==bot_choice):
        result="It's a draw. Try again"
    elif (user_choice=="rock" and bot_choice=="scissors" ) or (user_choice=="paper" and bot_choice=="rock") or (user_choice=="scissors" and bot_choice=="paper"):
        result="You Win!"
    else:
        result="You lose 😢"

    embed=discord.Embed(title="Rock Paper Scissors", description=f'The bot chose {bot_choice}. {result}',color=0x333333)
    await ctx.send(embed=embed)


#announce

@commands.command(name="announce")
@commands.has_permissions(administrator=True)
async def announce(ctx,*,message:str):
        
        await ctx.send(f'@everyone\n {message}')
        await ctx.message.delete()




@announce.error
async def announce_error(ctx,message:str):
        embed1 = discord.Embed(title="ERROR", description="You Don't Have The Required Permission To Use This Command", color=discord.Color.red())
        embed1.set_footer(text="Invite This Bot To Your Server To Access This Command")
        await ctx.send(embed=embed1)

        

    

    


