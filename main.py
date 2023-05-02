#------------------------MODULES-------------------------------------------------------------#
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
from modules import coinflip,meme,dice,qutoes,gambler,chat,gifs


load_dotenv()

DISCORD_KEY= os.getenv('DISCORD_ID')
#from discord import app_commands

#------------------------INITIALIZING THE BOT-------------------------------------------------#

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


#tree = app_commands.CommandTree(bot)
#..

@bot.event
async def on_ready():
    print("The bot is ready")
        
    
@bot.command(name="greet")
async def greet(ctx):
    """
    This is a greet command
    """
    await ctx.channel.send("good morning")

@bot.command(name="joke")
async def joke(ctx):
    """
    This is a joke
    """
    await ctx.channel.send("Your mama so fat, kadota is jealous of her")



bot.add_command(coinflip.coin_flip)
bot.add_command(meme.meme)
bot.add_command(dice.rolldice)
bot.add_command(qutoes.quote)
bot.add_command(qutoes.devjoke)
@bot.command(name = 'trivia')
async def play(ctx):
    await qutoes.trivia(ctx, bot)

#gmabler
bot.add_command(gambler.daily)
bot.add_command(gambler.balance)
bot.add_command(gambler.monie)
bot.add_command(gambler.bet)
bot.add_command(gambler.steal)

#gifs
bot.add_command(gifs.hug)
bot.add_command(gifs.slap)
bot.add_command(gifs.kiss)
bot.add_command(gifs.bite)
bot.add_command(gifs.lick)


bot.add_command(chat.learn)
bot.add_command(chat.c)



bot.run(DISCORD_KEY)




