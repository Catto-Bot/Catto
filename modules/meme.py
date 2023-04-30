#aryn
from discord.ext import commands
import json
import requests
import discord

@commands.command(name="meme")
async def meme(ctx):
    memejson = json.loads(
        requests.get("https://meme-api.com/gimme").text
        )

    
    embed = discord.Embed(
    title= memejson['title'],
    url = memejson['postLink'],
    )
    embed.set_image(url=memejson['url'])
    embed.set_footer(text=memejson['author'])
    meme = await ctx.send(embed=embed)
    await meme.add_reaction("👍")
    await meme.add_reaction("👎")

