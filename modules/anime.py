from discord.ext import commands
import discord
import requests

@commands.command(name="animeQuote")
async def animeQuote(ctx):
    try:
        api_url = 'https://animechan.vercel.app/api/random'
        response = requests.get(api_url)
        aniQuote = response.json()
        animeName = aniQuote['anime']
        
        aniChara = aniQuote ['character']
        
        mainQuote = aniQuote['quote']
        

        embed = discord.Embed(title=f"Anime Name: {animeName}",description= f"'{mainQuote}'", color=0x555555 )
        embed.set_footer(text=f"-{aniChara}")
        await ctx.send(embed = embed )
    except:
    
       await ctx.send( f"TATAKAE!🕊️- Eren Yeager" )


