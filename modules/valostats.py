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

    await ctx.send(display_names)
    
