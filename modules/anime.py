from discord.ext import commands
import discord
import requests
from admin import messages

@commands.command(name="animeQuote")
async def animeQuote(ctx):
    try:
        hello = await ctx.send("loading ")
        api_url = 'https://animechan.vercel.app/api/random'
        response = requests.get(api_url)
        aniQuote = response.json()
        animeName = aniQuote['anime']
        
        aniChara = aniQuote ['character']
        
        mainQuote = aniQuote['quote']
        

        embed = discord.Embed(title=f"Anime Name: {animeName}",description= f"'{mainQuote}'", color=0x555555 )
        embed.set_footer(text=f"-{aniChara}")
        await hello.delete()
        await ctx.send(embed = embed )
    except:
    
       await ctx.send( f"TATAKAE!🕊️- Eren Yeager" )

@commands.command()
async def something(ctx):
    embed = messages.WIP()
    await ctx.send(embed=embed)

