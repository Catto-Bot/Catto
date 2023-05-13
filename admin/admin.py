from discord.ext import commands
import discord
import time
import requests
import asyncio



@commands.command(name="ping")
async def ping(ctx):
    try:
        start_time = time.time()
        a = await ctx.send("Pinging")
        test1 = requests.get("https://icanhazdadjoke.com/slack")
        test2 = requests.get("https://meme-api.com/gimme")
        embed=discord.Embed(title="hehe", description="hehe")
        embed.add_field(name="hehe", value=test1)
        embed.add_field(name="hehe", value=test2)
        await a.edit(content="Almost Done!")
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        
        await ctx.send(f"Latency: {latency:.2f}ms")

    except Exception as err:
        await ctx.send("an error occured. please try again!")
        print(err)


# @commands.command(name="restart")
# async def restart(ctx):
#     numbers = [5,4,3,2,1]
#     countdown = await ctx.send("Restarting In")
#     await asyncio.sleep(1)
#     for num in numbers:
#         await countdown.edit(content = num)
#     await countdown.edit(content="Restarting..")
#     await ctx.bot.close()
#     await countdown.edit(content="Started..")


        
        



    