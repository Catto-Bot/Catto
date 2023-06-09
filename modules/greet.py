from discord.ext import commands
import discord
import json


def welcomemessage(message):
    welcomemessage = message
    return

def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")

@commands.command(name="setwelcomechannel")
@commands.has_permissions(administrator=True)
async def setwelcomechannel(ctx, channe_lid):
    save(ctx)
    try:
        channelid = channe_lid.strip('<#>')
        embed = discord.Embed(title="Success!", description="The default welcome channel has been set!")
        embed.set_footer(text="Thank you for using Catto Bot!")

        with open('channelgreet.json', 'r') as f:
            channelgreet = json.load(f)

        channelgreet[str(ctx.guild.id)] = str(channelid)

        with open('channelgreet.json', 'w') as f:
            json.dump(channelgreet, f, indent=4)

        await ctx.send(embed=embed)
    except Exception as err:
        await ctx.send(err)

@commands.command(name="deletewelcomechannel")
@commands.has_permissions(administrator=True)
async def deletewelcomechannel(ctx):
    save(ctx)
    try:
        embed = discord.Embed(title="Success!", description="The default welcome channel has been deleted!")
        embed.set_footer(text="Thank you for using Catto Bot!")

        with open('channelgreet.json', 'r') as f:
            channelgreet = json.load(f)

        del channelgreet[str(ctx.guild.id)]

        with open('channelgreet.json', 'w') as f:
            json.dump(channelgreet, f, indent=4)

        await ctx.send(embed=embed)
    except Exception as err:
        await ctx.send(err)


@commands.command(name="setleavechannel")
@commands.has_permissions(administrator=True)
async def setleavechannel(ctx, channe_lid):
    save(ctx)
    channelid = channe_lid.strip('<#>')
    try:
        embed = discord.Embed(title="Success!", description="The default leave channel has been set!")
        embed.set_footer(text="Thank you for using Catto Bot!")

        with open('channeleave.json', 'r') as f:
            channelgreet = json.load(f)

        channelgreet[str(ctx.guild.id)] = str(channelid)

        with open('channeleave.json', 'w') as f:
            json.dump(channelgreet, f, indent=4)

        await ctx.send(embed=embed)
    except Exception as err:
        await ctx.send(err)

@commands.command(name="deleteleavechannel")
@commands.has_permissions(administrator=True)
async def deleteleavechannel(ctx):
    save(ctx)
    try:
        embed = discord.Embed(title="Success!", description="The default leave channel has been deleted!")
        embed.set_footer(text="Thank you for using Catto Bot!")

        with open('channeleave.json', 'r') as f:
            channelgreet = json.load(f)

        del channelgreet[str(ctx.guild.id)]

        with open('channeleave.json', 'w') as f:
            json.dump(channelgreet, f, indent=4)

        await ctx.send(embed=embed)
    except Exception as err:
        await ctx.send(err)


@setleavechannel.error
async def setleavechannel_error(ctx,error):
    await ctx.send(error)

@deleteleavechannel.error
async def deleteleavechannel_error(ctx,error):
    await ctx.send(error)

@deletewelcomechannel.error
async def deletewelcomechannel_error(ctx,error):
    await ctx.send(error)
    
    
@setwelcomechannel.error
async def setwelcomechannel_error(ctx,error):
    await ctx.send(error)
    