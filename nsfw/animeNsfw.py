import discord
from discord.ext import commands
import requests
import random

def get_nsfw_channels(guild):
        for channel in guild.text_channels:
            if channel.is_nsfw():
                return channel
        return None


urls = ['https://api.waifu.im/search/?included_tags=ass', 'https://api.waifu.im/search/?included_tags=hentai', 'https://api.waifu.im/search/?included_tags=milf', 'https://api.waifu.im/search/?included_tags=waifu&is_nsfw=true', 'https://api.waifu.im/search/?included_tags=oppai&is_nsfw=true', 'https://api.waifu.im/search/?included_tags=selfies&is_nsfw=true', 'https://api.waifu.im/search/?included_tags=uniform&is_nsfw=true']

gifs = ['https://tenor.com/view/pervert-anime-gif-8409011','https://tenor.com/view/anime-kanna-you-perverts-pervert-gif-14346888', 'https://tenor.com/view/anime-yandere-creepy-peep-gif-20022951', 'https://tenor.com/view/caught-in-4k-caught-in4k-chungus-gif-19840038', 'https://tenor.com/view/anime-waiting-for-text-waiting-for-your-reply-gif-14108959','https://tenor.com/view/mirai-nikki-mao-mao-nonosaka-4k-caught-in4k-gif-23646198','https://tenor.com/view/kiniromozaic-kinmoza-pervert-you-pervert-mad-gif-5329720','https://tenor.com/view/kiniromozaic-kinmoza-pervert-you-pervert-mad-gif-5329720', 'https://tenor.com/view/anime-lewd-warning-nsfw-naughty-gif-8681415','https://tenor.com/view/nami-sanji-slap-one-piece-anime-gif-19985101']


@commands.command()
async def hentai(ctx):
    try: 
        guild = ctx.guild
        
        nsfw_channel = get_nsfw_channels(guild)

        if nsfw_channel == None:
            await ctx.send(random.choice(gifs))
            return
        
        if ctx.channel.id != nsfw_channel.id:
             await ctx.send('This is not a NSFW channel.😠')
             await ctx.send(random.choice(gifs))
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