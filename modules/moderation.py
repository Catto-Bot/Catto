from discord.ext import commands
import discord
import json
import requests
from time import sleep



#########################################################################
# STILL WORKING ON THIS SO JUST IGNORE THIS SHIT THAT IS GOING ON HERE 

#mute
@commands.command()
@commands.has_role('Judge')
async def mute(ctx, user: discord.Member, time):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send(str(user) + ' has been muted')
    
    # Wait a certain time before unmuting
    await sleep(int(time))
    await user.remove_roles(role)
    await ctx.send(str(user) + ' is unmuted')

# Ban users
@commands.command()
@commands.has_role('Judge')
async def ban(ctx, user: discord.Member):
    await user.ban()
    await ctx.send('The user has been banned')
    print('A user has been banned')

# Kick users
@commands.command()
@commands.has_role('Judge')
async def kick(ctx, user: discord.Member):
    await user.kick()
    await ctx.send('The user has been kicked out the server')

#########################################################################