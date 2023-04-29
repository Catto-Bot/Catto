#ghost
import requests
import json
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
import json



load_dotenv()

API_KEY= os.getenv('QUOTES_API_KEY')

@commands.command(name="quotes")
async def quotes(ctx,category):
    try:
        api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        if response.status_code == requests.codes.ok:
            data = response.json()
            quote = data[0]['quote']
            author = data[0]['author']
            embed = discord.Embed(title="", description=f"\"{quote}\"", color=0x555555)
            embed.set_footer(text=f"-{author}")

            await ctx.channel.send(embed=embed)
        else:
            raise Exception("Wrong category")
    except:
        await ctx.channel.send(f"I am feeling down myself today 🥲")
 
 
@commands.command(name="quote")
async def quote(ctx):
    try:
        api_url = f'https://api.api-ninjas.com/v1/quotes'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        if response.status_code == requests.codes.ok:
            data = response.json()
            quote = data[0]['quote']
            author = data[0]['author']
            category = data[0]['category']
            embed = discord.Embed(title=f"{category.capitalize()} Quote", description=f"\"{quote}\"", color=0x555555)
            embed.set_footer(text=f"-{author}")

            await ctx.channel.send(embed=embed)
        else:
            raise IndexError("Sorry, no numbers below zero")
    except:
        await ctx.channel.send("My API is down today 🤧")
    