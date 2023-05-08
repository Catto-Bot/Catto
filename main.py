#------------------------MODULES-------------------------------------------------------------#
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
import json
from modules import coinflip,meme,dice,qutoes,gambler,chat,gifs,ticket,valostats,avatar,fight,anime,prefix,moderation





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




intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)




@bot.event
async def on_ready():
    print("The bot is ready")


@bot.event
async def on_guild_join(guild): 
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f) 

    prefixes[str(guild.id)] = '>'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4) 

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)




bot.add_command(coinflip.coin_flip)
bot.add_command(coinflip.rps_game)
bot.add_command(coinflip.announce)
bot.add_command(meme.meme)
bot.add_command(dice.rolldice)
bot.add_command(dice.cat)
bot.add_command(qutoes.quote)
bot.add_command(qutoes.devjoke)
bot.add_command(qutoes.dadjoke)
bot.add_command(qutoes.trivia)
bot.add_command(qutoes.insult)
bot.add_command(qutoes.dark)
bot.add_command(qutoes.spooky)

#gmabler
bot.add_command(gambler.daily)
bot.add_command(gambler.weekly)
bot.add_command(gambler.balance)
bot.add_command(gambler.monie)
bot.add_command(gambler.bet)
bot.add_command(gambler.steal)


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
bot.add_command(gifs.kick)
bot.add_command(gifs.wink)
bot.add_command(gifs.poke)


bot.add_command(chat.learn)
bot.add_command(chat.c)


bot.add_command(ticket.ticketsetup)
bot.add_command(ticket.deleteticket)


bot.add_command(valostats.vstats)
bot.add_command(valostats.maps)

bot.add_command(avatar.avatar)

bot.add_command(fight.fight)

bot.add_command(anime.animeQuote)

bot.add_command(prefix.setprefix)
bot.add_command(prefix.prefix)

bot.add_command(moderation.mute)


bot.run(DISCORD_KEY)




