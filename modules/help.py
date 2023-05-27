from discord.ext import commands
import discord
import json
import datetime

def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")

@commands.command(name="help")
async def help(ctx):
    save(ctx)
    with open("prefixes.json", "r") as read:
        prefixes = json.load(read)

    embed = discord.Embed(title="Catto Commands", description="Here are the available commands:")
    embed.add_field(name="👨‍💻 Main", value="info, ai(prompt), uptime", inline=False)
    embed.add_field(name="😼 AniCat", value="anicat, anicatstats, anicatinfo", inline=False)
    embed.add_field(name="💰 CattoGamble", value="monie, balance, daily, weekly, bet, steal, leaderboard, give", inline=False)
    embed.add_field(name="🎮 ValoStats", value="vstats, valofight", inline=False)
    embed.add_field(name="💬 Chat", value="chat, learn", inline=False)
    embed.add_field(name="🐱 Anime", value="animeQuote", inline=False)
    embed.add_field(name="🖼️ Avatar", value="avatar", inline=False)
    embed.add_field(name="✨ Emojify", value="emojify", inline=False)
    embed.add_field(name="💨 NSFW", value="hentai, nsfw (prompt), hdnsfw", inline=False)
    embed.add_field(name="🎥 Gifs", value="hug, slap, kiss, lick, bite, bully, blush, cry, cuddle, smug, bonk, pat, handhold, nom, kill, wink, poke", inline=False)
    embed.add_field(name="👋 Greet", value="setwelcomechannel, setupleavechannel", inline=False)
    embed.add_field(name="🎭 Meme", value="meme, darkmeme, dadjoke, devjoke, bored", inline=False)
    embed.add_field(name="🔨 Games", value="trivia, hangman", inline=False)
    embed.add_field(name="🔨 Moderation", value="mute, kick, ban, unmute", inline=False)
    embed.add_field(name="⚙️ Prefix", value="prefix, setprefix", inline=False)
    embed.add_field(name="📜 Quotes", value="quote, insult, spooky, advice", inline=False)
    embed.add_field(name="🔒 Roles", value="setuprole, createrole, removerole, deleterole", inline=False)
    embed.add_field(name="🎫 Ticket", value="ticketsetup, deleteticket", inline=False)
    embed.add_field(name="❓ Would You Rather?", value="wyr, truth, dare", inline=False)
    embed.add_field(name="🎲 Other", value="flip, rps, announce, cat, rolldice, ship, catfact, fakeinfo", inline=False)
    embed.set_footer(text=f"Current Prefix: {prefixes[str(ctx.guild.id)]}")

    embed.color = discord.Color.blue() 
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed.set_footer(text=f"Prefix Set For This Server: {prefixes[str(ctx.guild.id)]} | Generated at: {current_time}")

    await ctx.send(embed=embed)


