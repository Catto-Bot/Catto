#------------------------MODULES-------------------------------------------------------------#
import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
import json





load_dotenv()

DISCORD_KEY= os.getenv('DISCORD_ID')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
@bot.event
async def on_ready():
    print("The bot is ready")

@bot.event
async def on_message(message):
    await message.channel.send("Bot Offline!")









bot.run(DISCORD_KEY)




