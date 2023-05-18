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
            mute_role = await ctx.guild.create_role(name='Timeout', reason='Needed to Mute', color =0x0ff)

            # Loop through the channels in the server and deny the mute role from sending messages
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)
        
        # Wait a certain time before unmuting
        await user.add_roles(mute_role, reason=f'Timeout for {time} minute')
        await ctx.send(str(user.mention) + ' has been muted')

        await asyncio.sleep(int(time)*60)

        await user.remove_roles(mute_role)
        await ctx.send(str(user.mention) + ' has been unmuted')
        
    except Exception as err:
        print(err)

# Ban users
@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member):
    await user.ban()
    await ctx.send(f'The user ({user}) has been banned')

# Kick users
@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
    await user.kick()
    await ctx.send(f'The user ({user}) has been kicked out of the server')

# Unmute users
@commands.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, user: discord.Member):
    try:
  
        mute_role = discord.utils.get(ctx.guild.roles, name='muted')

        if mute_role is None:
            raise Exception

        if mute_role in user.roles:
            await user.remove_roles(mute_role)
            return
        embeded = discord.Embed(title="This user is not muted.", description='Do you want me to mute this user? 🤔', color=0x555555)
        joke = await ctx.send(embed = embeded)

        await asyncio.sleep(5)

        embeded.set_footer(text="Error")
        await joke.edit(embed = embeded)
       
        
    except Exception as err:
        embeded = discord.Embed(title='First use !mute <User> to use the unmute command"')
        await ctx.send(embed = embeded)
#########################################################################

@mute.error
async def mute_error(ctx,err):
    embed = discord.Embed(title=err, description="")
    await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx,err):
    embed = discord.Embed(title=err, description="")
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx,err):
    embed = discord.Embed(title=err, description="")
    await ctx.send(embed=embed)

@unmute.error
async def unmute_error(ctx,err):
    embed = discord.Embed(title=err, description="")
    await ctx.send(embed=embed)