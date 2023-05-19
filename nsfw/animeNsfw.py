import discord
from discord.ext import commands
import requests
import random
def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")

def get_nsfw_channels(guild):
        for channel in guild.text_channels:
            if channel.is_nsfw():
                return channel
        return None


urls = ['https://api.waifu.im/search/?included_tags=ass', 'https://api.waifu.im/search/?included_tags=hentai', 'https://api.waifu.im/search/?included_tags=milf', 'https://api.waifu.im/search/?included_tags=waifu&is_nsfw=true', 'https://api.waifu.im/search/?included_tags=oppai&is_nsfw=true', 'https://api.waifu.im/search/?included_tags=selfies&is_nsfw=true', 'https://api.waifu.im/search/?included_tags=uniform&is_nsfw=true']

gifs = ['https://media.tenor.com/n1kNXs7w8q8AAAAd/pervert-anime.gif','https://media.tenor.com/t2pLAIENp_EAAAAC/anime-kanna.gif', 'https://media.tenor.com/BuA6tck7eTEAAAAC/anime-yandere.gif', 'https://media.tenor.com/QA6mPKs100UAAAAC/caught-in.gif', 'https://media.tenor.com/8yMqNs21uTQAAAAd/anime-waiting-for-text.gif','https://media.tenor.com/cKwZeGp3uMQAAAAC/mirai-nikki-mao.gif','https://media.tenor.com/JFUBQIDFTvcAAAAC/kiniromozaic-kinmoza.gif','https://media.tenor.com/JFUBQIDFTvcAAAAC/kiniromozaic-kinmoza.gif', 'https://media.tenor.com/6J2mC84fUtsAAAAC/anime-lewd.gif','https://media.tenor.com/00huTPPw5HIAAAAC/nami-sanji.gif']


@commands.command()
async def hentai(ctx):
    save(ctx)
    try:
        guild = ctx.guild
        
        nsfw_channel = get_nsfw_channels(guild)

        if nsfw_channel == None:
            await ctx.send(random.choice(gifs))
            return
        
        if ctx.channel.id != nsfw_channel.id:
             embed= discord.Embed(title="This is not a NSFW channel!!😠", description="")
             embed.set_image(url=random.choice(gifs))
             await ctx.send(embed=embed)
             return
        
        response = requests.get(random.choice(urls))
        data = response.json()
        url = data['images'][0]['url']
        embed = discord.Embed(title='',color=0x333333)
        embed.set_image(url = url)

        await nsfw_channel.send(embed = embed)
    except Exception as err:
         print(err)
         embed = discord.Embed(color = 0xff7b7b)
         embed.set_image(url = "https://tenor.com/view/anime-kanna-you-perverts-pervert-gif-14346888")
         await ctx.send(embed = embed)