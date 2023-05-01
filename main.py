
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
import sqlite3
from modules import coinflip,meme,dice,qutoes,gambler,fight,chat


load_dotenv()
DISCORD_KEY= os.getenv('DISCORD_ID')


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)




@bot.event
async def on_ready():
    print("The bot is ready")


        
    




bot.add_command(coinflip.coin_flip)
bot.add_command(meme.meme)
bot.add_command(dice.rolldice)
bot.add_command(qutoes.quote)
@bot.command(name = 'trivia')
async def play(ctx):
    await qutoes.trivia(ctx, bot)

#gmabler
bot.add_command(gambler.daily)
bot.add_command(gambler.balance)
bot.add_command(gambler.monie)
bot.add_command(gambler.bet)
bot.add_command(gambler.steal)
bot.add_command(gambler.test)

bot.add_command(fight.button)

bot.add_command(chat.learn)
bot.add_command(chat.c)



bot.run(DISCORD_KEY)




