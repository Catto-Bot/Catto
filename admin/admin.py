from discord.ext import commands
import discord
import time
import requests
import asyncio
from datetime import datetime
import os



bot_version = "2.0"
github_repo = "Soon To Be Public"

@commands.command(name="info")
async def info(ctx):
    devs = ["Ghost Riley#6077", "Nitrix#1271", "kadota#1408", "aryn#5511"]
    dev_names = "\n".join(devs)
    
    embed = discord.Embed(
        title="Developers",
        description=dev_names,
        color=0x000000
    )
    embed.add_field(name="Bot Version", value=bot_version, inline=False)
    embed.add_field(name="Coded in", value="``discord.py``", inline=False)
    embed.add_field(name="Github Repo", value="``https://github.com/Catto-Bot/Catto``", inline=False)
    embed.add_field(name="Support Server", value="``https://discord.gg/cvNa9XTbD9``", inline=False)
    embed.set_footer(
        text=f"Requested by {ctx.message.author.display_name}",
        icon_url=ctx.message.author.avatar
    )
    
    await ctx.send(embed=embed)



@commands.command(name="ping")
async def ping(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
    try:
        start_time = time.time()
        a = await ctx.send("Pinging")
        test1 = requests.get("https://icanhazdadjoke.com/slack")
        embed=discord.Embed(title="hehe", description="hehe")
        embed.add_field(name="hehe", value=test1)
        await a.edit(content="Almost Done!")
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        latencybot = ctx.bot.latency 
        embed = discord.Embed(title="Bot Latency", description="")
        embed.add_field(name="Server/Api Latency", value=f"Latency: {latency:.2f}ms", inline=False)
        embed.add_field(name="Actual Bot Latency", value=f'Pong! Latency: {latencybot * 1000:.2f}ms', inline=False)
        await a.delete()
        await ctx.send(embed=embed)
        
    except Exception as err:
        await ctx.send("an error occured. please try again!")
        print(err)

@commands.command(name="servers")
@commands.check(lambda ctx: ctx.author.id == 780639741866409984 or ctx.author.id == 534977801116319745 or ctx.author.id == 540405934367703050 or ctx.author.id == 582506141959979008)
async def servers(ctx):
    a = 0
    total_members = 0
    server_info = ""
    
    for guild in ctx.bot.guilds:
        server_info += f"#{a}, {guild}, {guild.member_count}, id = {guild.id}\n"
        a += 1
        total_members += guild.member_count

    with open("server_info.txt", "w") as file:
        file.write(server_info)

    await ctx.send(f"Server information for {ctx.bot.user.name} ({len(ctx.bot.guilds)} servers, {total_members} members)", file=discord.File("server_info.txt"))

    os.remove("server_info.txt")







@commands.command(name="addai")
@commands.check(lambda ctx: ctx.author.id == 780639741866409984)
async def addai(ctx, msg):
    try:
        with open("ai_allowed.txt", "a") as file:
            file.write(msg + "\n")
        await ctx.send("done")
    except Exception as err:
        await ctx.send(err)



   




@commands.command(name="invite")
async def invite(ctx):
    print(f"ping command used in '{ctx.guild.name}' Server By {ctx.author}")
    embed = discord.Embed(title="Invite Our Bot To Your Server!", description="https://discord.com/oauth2/authorize?client_id=1108380972950491146&permissions=8&scope=bot")
    embed.set_footer(text="Thank You For Using Catto0!")
    await ctx.send(embed=embed)
 


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

@addai.error
async def addai_error(ctx,error):
    await ctx.send("This command can only be used by aryn#5511")
        
        
@servers.error
async def servers_error(ctx,error):
    print(error)
    await ctx.send("This command can only be used by aryn#5511")


    