#ghost
import discord
from discord.ext import commands
import requests

API_KEY ='aEIxt6NSkJGib80neq+dRg==p1ytbEYfgbfg9zBW'

@commands.command(name="quotes")
async def quotes(ctx, category):
    try:
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        if response.status_code == requests.codes.ok:
            data = response.json()[0]
            quotes = data['quote']
            author = data['author']
            embed = discord.Embed(title="", description=f"\"{quotes}\"", color=0x555555)
            embed.set_footer(text=f"-{author}")
            await ctx.channel.send(embed=embed)
        else:
            raise Exception("Sorry")
    except:
        await ctx.channel.send("I am down myself 🥲")


@commands.command(name="quote")
async def quote(ctx):
    try:
        api_url = 'https://api.api-ninjas.com/v1/quotes'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        print(response)
        if response.status_code == requests.codes.ok:
            data = response.json()[0]
            quotes = data['quote']
            author = data['author']
            category = data['category']
            embed = discord.Embed(title=f"{category.capitalize()} Quote", description=f"\"{quotes}\"", color=0x555555)
            embed.set_footer(text=f"-{author}")
            quote = await ctx.channel.send(embed=embed)
            await quote.add_reaction("👍")
            await quote.add_reaction("👎")
        else:
            raise Exception("Sorry")
    except:
        await ctx.channel.send(f"I am down myself 🥲")
