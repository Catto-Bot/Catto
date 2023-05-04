from discord.ext import commands
import discord
import json
import requests


@commands.command(name="hug")
async def hug(ctx, member: commands.MemberConverter = None):
    if member:
        hugr = requests.get("https://purrbot.site/api/img/sfw/hug/gif")
        json_hug_data = json.loads(hugr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} hugs {member.display_name}! AWWWWW ❁◕ ‿ ◕❁", color=discord.Color.dark_gray())
        embed.set_image(url=json_hug_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Hugged Yourself! ❁◕ ‿ ◕❁")
         embed.set_footer(text="Next Time Mention A User To Hug :D")
         embed.set_image(url="https://media.tenor.com/XEEmDlNSmEcAAAAM/spongebob-love.gif")
         await ctx.send(embed=embed)

@commands.command(name="slap")
async def slap(ctx, member: commands.MemberConverter = None):
    if member:
        hugr = requests.get("https://purrbot.site/api/img/sfw/slap/gif")
        json_hug_data = json.loads(hugr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} slaps {member.display_name}! OUCH ( ಥ۝ಥ )", color=discord.Color.dark_gray())
        embed.set_image(url=json_hug_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You slapped Yourself! ( ಥ۝ಥ )")
         embed.set_footer(text="Next Time Mention A User To Slap :D")
         embed.set_image(url="https://media.tenor.com/rXAnv88yrFwAAAAM/anime-slapping-face.gif")
         await ctx.send(embed=embed)

@commands.command(name="kiss")
async def kiss(ctx, member: commands.MemberConverter = None):
    if member:
        hugr = requests.get("https://purrbot.site/api/img/sfw/kiss/gif")
        json_hug_data = json.loads(hugr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} kisses {member.display_name}! AWWWW (ᅌwᅌ)", color=discord.Color.dark_gray())
        embed.set_image(url=json_hug_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Can't Kiss Yourself! ( ಥ۝ಥ )")
         embed.set_footer(text="Next Time Mention A User To Kiss :D")
         await ctx.send(embed=embed)

@commands.command(name="bite")
async def bite(ctx, member: commands.MemberConverter = None):
    if member:
        biter = requests.get("https://purrbot.site/api/img/sfw/bite/gif")
        json_bite_data = json.loads(biter.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} bites {member.display_name}! OUCH! (ಥ۝ಥ)", color=discord.Color.dark_gray())
        embed.set_image(url=json_bite_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Bit Yourself! ( ಥ۝ಥ )")
         embed.set_image(url="https://media.tenor.com/D7XNyUe6Q7UAAAAS/hit-self-kitten.gif")
         embed.set_footer(text="Next Time Mention A User To Kiss :D")
         await ctx.send(embed=embed)

@commands.command(name="lick")
async def lick(ctx, member: commands.MemberConverter = None):
    if member:
        lickr = requests.get("https://purrbot.site/api/img/sfw/lick/gif")
        json_lick_data = json.loads(lickr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} Licks {member.display_name}! AWWWWW! (✿ ♥‿♥)(♥ω♥*)", color=discord.Color.dark_gray())
        embed.set_image(url=json_lick_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Licked Yourself! ♥‿♥")
         embed.set_image(url="https://media.tenor.com/6StCIWYFkOcAAAAC/adalfarus-adal.gif")
         embed.set_footer(text="Next Time Mention A User To Lick :D")
         await ctx.send(embed=embed)



