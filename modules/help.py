from discord.ext import commands
import discord
import json
import datetime

@commands.command(name="help")
async def help(ctx):
    with open("prefixes.json", "r") as read:
        prefixes = json.load(read)
    
    embed = discord.Embed(title="Catto Commands", description="Here are the available commands:")
    embed.add_field(name="💰 CattoGamble", value="monie, balance, daily, weekly, bet, steal, leaderboard", inline=False)
    embed.add_field(name="🎮 ValoStats", value="vstats, maps, valofight", inline=False)
    embed.add_field(name="💬 Chat", value="learn, c", inline=False)
    embed.add_field(name="🐱 Anime", value="animeQuote", inline=False)
    embed.add_field(name="🖼️ Avatar", value="avatar", inline=False)
    embed.add_field(name="✨ Emojify", value="emojify", inline=False)
    embed.add_field(name="👤 FakeInfo", value="fakeinfo", inline=False)
    embed.add_field(name="🎥 Gifs", value="hug, slap, kiss, lick, bite, bully, blush, cry, cuddle, smug, bonk, pat, handhold, nom, kill, wink, poke", inline=False)
    embed.add_field(name="👋 Greet", value="setwelcomechannel, setupleavechannel", inline=False)
    embed.add_field(name="🎭 Meme", value="meme, darkmeme, dadjoke, devjoke", inline=False)
    embed.add_field(name="🔨 Moderation", value="mute, kick, ban, unmute", inline=False)
    embed.add_field(name="⚙️ Prefix", value="prefix, setprefix", inline=False)
    embed.add_field(name="📜 Quotes", value="quote, trivia, insult, spooky, advice", inline=False)
    embed.add_field(name="🔒 Roles", value="setuprole, createrole, removerole, deleterole", inline=False)
    embed.add_field(name="🎫 Ticket", value="ticketsetup, deleteticket", inline=False)
    embed.add_field(name="❓ Would You Rather?", value="wyr", inline=False)
    embed.add_field(name="🎲 Other", value="flip, rps, announce, jokes, cat, rolldice", inline=False)
    embed.set_footer(text=f"Current Prefix: {prefixes[str(ctx.guild.id)]}")

    embed.color = discord.Color.blue() 
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed.set_footer(text=f"Prefix Set For This Server: {prefixes[str(ctx.guild.id)]} | Generated at: {current_time}")

    await ctx.send(embed=embed)


