# aryn
import json

import discord
import requests
from discord.ext import commands


@commands.command(name="meme")
async def meme(ctx):
    try:
        ret = await ctx.send("Checking The Database For Memes. <a:loading:1108012790783946772>")
        memejson = json.loads(requests.get("https://meme-api.com/gimme").text)

        embed = discord.Embed(
            title=memejson["title"],
            url=memejson["postLink"],
        )
        embed.set_image(url=memejson["url"])
        embed.set_footer(text=memejson["author"])
        await ret.delete()
        meme = await ctx.send(embed=embed)
        await meme.add_reaction("👍")
        await meme.add_reaction("👎")
    except Exception:
        await ctx.send("There was an error!")
