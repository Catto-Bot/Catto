from discord.ext import commands
import discord
import random
import json
import requests
from rule34Py import rule34Py

def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")

def get_nsfw_channels(guild):
        nsfws = []
        for channel in guild.text_channels:
            if channel.is_nsfw():
                nsfws.append(channel)
        return nsfws


@commands.command(name="hdnsfw")
async def hdnsfw(ctx):
    nsfw_channels = get_nsfw_channels(ctx.guild)
    if nsfw_channels == []:
        await ctx.send('This server doesn\'t have any nsfw channel.')
        return
    if ctx.channel.id in [channel.id for channel in nsfw_channels]:
        save(ctx)
        pickone = ["4k"]
        forjson = "http://api.nekos.fun:8080/api/"+random.choice(pickone)
        requestjson = requests.get(forjson).text
        data = json.loads(requestjson)
        image_url = data['image']
        embed = discord.Embed(title="Here is A Random 4k NSFW Image", description="")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        embed= discord.Embed(title="Not an NSFW Channel..Aborting", description="")
        await ctx.send(embed=embed)


@commands.command(name="nsfw")
async def nsfw(ctx, *, args=None):
    save(ctx)
    nsfw_channels = get_nsfw_channels(ctx.guild)
    if nsfw_channels == []:
        await ctx.send('This server doesn\'t have any nsfw channel.')
        return
    if ctx.channel.id in [channel.id for channel in nsfw_channels]:
        if args is not None and args.strip():
            try:
                connecting = await ctx.send("``Connecting To Api``")
                r34Py = rule34Py()
                search_tags = args.split()  # Split args into individual words
                result_random = r34Py.random_post(search_tags)
                embed = discord.Embed(title="RULE 34", description=f"ID: {result_random.id}")
                embed.set_image(url=result_random.image)
                await connecting.edit(content="``Almost Done``")
                embed.set_footer(
                    text=f"Requested by {ctx.message.author.display_name}",
                    icon_url=ctx.message.author.avatar
                )
                await connecting.delete()
                await ctx.send(embed=embed)
            except Exception as err:
                embed = discord.Embed(title="Error!", description=str(err))
                await ctx.send(embed=embed)
        else:
            connecting = await ctx.send("``Connecting To Api For A Random NSFW Image``")
            r34Py = rule34Py()
            result_random = r34Py.random_post()
            embed = discord.Embed(title="RULE 34", description=f"ID: {result_random.id}")
            embed.set_image(url=result_random.image)
            await connecting.edit(content="``Almost Done``")
            embed.set_footer(
                    text=f"Requested by {ctx.message.author.display_name}",
                    icon_url=ctx.message.author.avatar
            )
            await connecting.delete()
            await ctx.send(embed=embed)
    else:
        embed= discord.Embed(title="Not an NSFW Channel..Aborting", description="")
        await ctx.send(embed=embed)

        


@nsfw.error
async def nsfw_error(ctx,err):
        embed = discord.Embed(title="Error!", description=err)
        await ctx.send(embed=embed)