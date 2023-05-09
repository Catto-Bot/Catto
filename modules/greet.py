from discord.ext import commands
import discord
import json


def welcomemessage(message):
    welcomemessage = message
    return

@commands.command(name="setwelcome")
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channelid):
    embed = discord.Embed(title="Success!", description="The default welcome message has been set!")
    embed.set_footer(text="Thank you for using Catto Bot!")

    with open('channelgreet.json', 'r') as f:
        channelgreet = json.load(f)

    channelgreet[str(ctx.guild.id)] = str(channelid)

    with open('channelgreet.json', 'w') as f:
        json.dump(channelgreet, f, indent=4)

    await ctx.send(embed=embed)

