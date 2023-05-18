from discord.ext import commands
import json
import discord


@commands.command(pass_context=True ,name="setprefix")
@commands.has_permissions(administrator=True) 
async def setprefix(ctx, prefix): 
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}') 
    name=f'{prefix}BotBot'

@commands.command(name="prefix")
async def prefix(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    embed = discord.Embed(title="Prefix", description=f"The Prefix For This Server Is '{prefixes[str(ctx.guild.id)]}'")
    await ctx.send(embed=embed)
    

@setprefix.error
async def setprefix_error(ctx,err):
    embed = discord.Embed(title="", description=err)
    await ctx.send(embed = embed)