import discord
from discord.ext import commands
import requests
import random

def get_nsfw_channels(guild):
        for channel in guild.text_channels:
            if channel.is_nsfw():
                return channel
        return None


urls = ['https://api.waifu.im/search/?included_tags=ass', 'https://api.waifu.im/search/?included_tags=hentai', 'https://api.waifu.im/search/?included_tags=milf']


@commands.command()
async def hentai(ctx):
    try: 
        guild = ctx.guild
        
        nsfw_channel = get_nsfw_channels(guild)

        if nsfw_channel == None:
            embed = discord.Embed(title='This server doesn\'t have any nsfw channels.')
            embed.set_image(url = "https://tenor.com/view/anime-kanna-you-perverts-pervert-gif-14346888")
            await ctx.send(embed= embed)
            return
        
        response = requests.get(random.choice(urls))
        data = response.json()
        url = data['images'][0]['url']
        embed = discord.Embed(title='I am watching you pervert 🤨',color=0x333333)
        embed.set_image(url = url)

        await nsfw_channel.send(embed = embed)
    except Exception as err:
         print(err)
         embed = discord.Embed(color = 0xff7b7b)
         embed.set_image(url = "https://tenor.com/view/anime-kanna-you-perverts-pervert-gif-14346888")
         await ctx.send(embed = embed)