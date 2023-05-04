from discord.ext import commands
import discord
import requests
import json

@commands.command(name="maps")
async def maps(ctx):
    response = requests.get('https://valorant-api.com/v1/maps')
    json_data = response.json()

    display_names = []

    for map_data in json_data['data']:
        if 'displayName' in map_data and map_data['displayName']:
            display_names.append(map_data['displayName'])

    random = await ctx.send(display_names)
    await random.delete()


@commands.command(name="vstats")
async def vstats(ctx, name):
    username,tag = name.split('#')
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}").text
    rankresponse = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{username}/{tag}").text
    valorant_stats = json.loads(response)
    rank_stats = json.loads(rankresponse)
    parse = valorant_stats['data']
    rankparse = rank_stats['data']
    images = rankparse["images"]
    cards = parse['card']
    embed = discord.Embed(
        title=f"{parse['name']} #{parse['tag']}",
        description=f"Account level: {parse['account_level']}"
    )
    embed.set_image(url=cards["wide"])
    embed.set_footer(text=f"Last Updated: {parse['last_update']} ")
    embed.set_thumbnail(url=images["small"])
    await ctx.send(embed=embed)


@vstats.error
async def vstats_error(ctx,name):
    embed= discord.Embed(title="Error!", description=f"Error While Retrieving Data. Please Try Again Later")
    embed.add_field(inline=False, name="Format", value="The Correct Format is !vstats (username#tagline)")
    embed.set_footer(text="Thank You For Using Catto!")
    await ctx.send(embed=embed)








    
