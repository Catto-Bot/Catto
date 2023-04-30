import discord
from discord.ext import commands
import random
import json
import time

@commands.command(name="daily")
async def daily(ctx):
    with open("catomonie.json","r") as f:
        catomonie = json.load(f)
    user_id = str(ctx.author.id)
    lastClaimed = catomonie.get(user_id,0)
    currentTime = time.time()
    if currentTime - lastClaimed >= 86400:
        if user_id not in catomonie:
            await ctx.send("Welcome to catto gabmble \n !gamble to start gambling \n !daily to claim your daily coins")
            catomonie[user_id] = {"coins": 0, "last_claimed": 0}
        catomonie[user_id]["coins"] += 100
        catomonie[user_id]["last_claimed"] = currentTime
        with open("catomonie.json","w") as final:
            json.dump(catomonie,final)
        await ctx.send("You earned 100 catomonie!")
    else:
  	    await ctx.send("You can claim catomonie once every 24 hours!")
