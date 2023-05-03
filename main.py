#------------------------MODULES-------------------------------------------------------------#
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
from modules import coinflip,meme,dice,qutoes,gambler,chat,gifs,ticket





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
bot.add_command(meme.meme)
bot.add_command(dice.rolldice)
bot.add_command(qutoes.quote)
bot.add_command(qutoes.devjoke)
@bot.command(name = 'trivia')
async def play(ctx):
    await qutoes.trivia(ctx, bot)

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









bot.run(DISCORD_KEY)




