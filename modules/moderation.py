from discord.ext import commands
import discord
import json
import requests
from time import sleep
import asyncio



#########################################################################
# COMPLETED 😁😁😁😁

#mute
@commands.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, user: discord.Member, time):
    try:
  
        mute_role = discord.utils.get(ctx.guild.roles, name='Timeout')

        if not mute_role:
            mute_role = await ctx.guild.create_role(name='Timeout', reason='Needed for muting', color =0x0ff)

            # Loop through the channels in the server and deny the mute role from sending messages
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)
        
        # Wait a certain time before unmuting
        await user.add_roles(mute_role, reason=f'Timeout for {time} minute')
        await ctx.send(str(user.mention) + ' is muted')

        await asyncio.sleep(int(time)*60)

        await user.remove_roles(mute_role)
        await ctx.send(str(user.mention) + ' is unmuted')
        
    except Exception as err:
        print(err)

# Ban users
@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member):
    await user.ban()
    await ctx.send(f'The user ({user}) has banned')

# Kick users
@commands.command()
@commands.has_permissions(kick_members=True)
async def kickthat(ctx, user: discord.Member):
    await user.kick()
    await ctx.send(f'The user ({user}) has been kicked out the server')

#########################################################################