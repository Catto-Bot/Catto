#------------------------MODULES-------------------------------------------------------------#
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
from modules import coinflip,meme,dice,qutoes
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
bot.add_command(dice.quotes)
bot.add_command(dice.quote)


bot.run(DISCORD_KEY)




