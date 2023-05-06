#------------------------MODULES-------------------------------------------------------------#
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
import json
from modules import coinflip,meme,dice,qutoes,gambler,chat,gifs,ticket,valostats,avatar,fight





load_dotenv()

DISCORD_KEY= os.getenv('DISCORD_ID')
#from discord import app_commands

#------------------------INITIALIZING THE BOT-------------------------------------------------#

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)




@bot.event
async def on_ready():
    print("The bot is ready")








bot.add_command(coinflip.coin_flip)
bot.add_command(coinflip.rps_game)
bot.add_command(coinflip.announce)
bot.add_command(meme.meme)
bot.add_command(dice.rolldice)
bot.add_command(dice.animeQuote)
bot.add_command(dice.cat)
bot.add_command(dice.anime)
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

bot.add_command(chat.learn)
bot.add_command(chat.c)


bot.add_command(ticket.ticketsetup)
bot.add_command(ticket.deleteticket)


bot.add_command(valostats.vstats)
bot.add_command(valostats.maps)

bot.add_command(avatar.avatar)

bot.add_command(fight.fight)









bot.run(DISCORD_KEY)




