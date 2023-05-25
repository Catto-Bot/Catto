#------------------------MODULES-------------------------------------------------------------#
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
import json
from events import events
from modules import coinflip,meme,dice,qutoes,gambler,chat,gifs,ticket,valostats,avatar,anime,prefix,moderation,greet,roles,wyr,emoji,fakeinfo,help,ship,conf,image_generation,hangman
from admin import admin
from anicat import anicat
from nsfw import animeNsfw
import time
import datetime





load_dotenv()

DISCORD_KEY= os.getenv('DISCORD_ID')
#from discord import app_commands

def get_prefix(bot, message): 
    try:
        with open('prefixes.json', 'r') as f: 
            prefixes = json.load(f) 
        return prefixes[str(message.guild.id)] 
    except:
        prefixes = {}

start_time = time.time() 


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)
bot.remove_command('help')
@bot.event
async def on_ready():
    print("The bot is ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
    


events.setup(bot)

@commands.command(name="uptime")
async def uptime(ctx):
    try:
        end_time = time.time()
        uptime = end_time - start_time

        weeks, uptime = divmod(uptime, 604800)  
        days, uptime = divmod(uptime, 86400)    
        hours, uptime = divmod(uptime, 3600)     
        minutes, seconds = divmod(uptime, 60)

        uptime_str = f"{int(weeks)} weeks, {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
        await ctx.send(f"Bot uptime: ``{uptime_str}``")
    except Exception as err:
        await ctx.send(f"An error occurred while retrieving the uptime: {err}")







bot.add_command(uptime)
bot.add_command(coinflip.coin_flip)
bot.add_command(coinflip.rps_game)
bot.add_command(coinflip.announce)
bot.add_command(coinflip.joke)
bot.add_command(coinflip.catfact)
bot.add_command(coinflip.bored)
bot.add_command(meme.meme)
bot.add_command(dice.rolldice)
bot.add_command(dice.cat)
bot.add_command(qutoes.quote)
bot.add_command(qutoes.devjoke)
bot.add_command(qutoes.dadjoke)
bot.add_command(qutoes.trivia)
bot.add_command(qutoes.insult)
bot.add_command(qutoes.darkmeme)
bot.add_command(qutoes.spooky)
bot.add_command(qutoes.advice)

#gmabler
bot.add_command(gambler.daily)
bot.add_command(gambler.weekly)
bot.add_command(gambler.balance)
bot.add_command(gambler.monie)
bot.add_command(gambler.bet)
bot.add_command(gambler.steal)
bot.add_command(gambler.leaderboard)
bot.add_command(gambler.give)


bot.add_command(gifs.hug)
bot.add_command(gifs.slap)
bot.add_command(gifs.kiss)
bot.add_command(gifs.lick)
bot.add_command(gifs.bite)
bot.add_command(gifs.bully)
bot.add_command(gifs.blush)
bot.add_command(gifs.cry)
bot.add_command(gifs.cuddle)
bot.add_command(gifs.smug)
bot.add_command(gifs.bonk)
bot.add_command(gifs.pat)
bot.add_command(gifs.handhold)
bot.add_command(gifs.nom)
bot.add_command(gifs.kill)
bot.add_command(gifs.wink)
bot.add_command(gifs.poke)


bot.add_command(chat.learn)
bot.add_command(chat.c)


bot.add_command(ticket.ticketsetup)
bot.add_command(ticket.deleteticket)


bot.add_command(valostats.vstats)
bot.add_command(valostats.valofight)


bot.add_command(avatar.avatar)


bot.add_command(anime.animeQuote)
bot.add_command(anime.something)

bot.add_command(prefix.setprefix)
bot.add_command(prefix.prefix)

bot.add_command(moderation.mute)
bot.add_command(moderation.kick)
bot.add_command(moderation.ban)
bot.add_command(moderation.unmute)

bot.add_command(roles.setuprole)
bot.add_command(roles.createrole)
bot.add_command(roles.removerole)
bot.add_command(roles.deleterole)

bot.add_command(wyr.wyr)



bot.add_command(greet.setwelcomechannel)
bot.add_command(greet.setleavechannel)


bot.add_command(admin.ping)
bot.add_command(admin.servers)
bot.add_command(admin.info)
bot.add_command(admin.invite)
bot.add_command(admin.addai)

bot.add_command(anicat.anicat)
bot.add_command(anicat.anicatstats)
bot.add_command(anicat.anicatinfo)

bot.add_command(fakeinfo.fakeinfo)

bot.add_command(emoji.emojify)

bot.add_command(help.help)
bot.add_command(ship.ship)

bot.add_command(conf.confessionsetup)
bot.add_command(conf.ch)

bot.add_command(animeNsfw.hentai)

bot.add_command(image_generation.ai)

bot.add_command(hangman.hangman)
bot.add_command(hangman.guess)








bot.run(DISCORD_KEY)




