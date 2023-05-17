from discord.ext import commands
import discord
import json
from datetime import datetime

@commands.command(name="confessionsetup")
@commands.has_permissions(administrator=True) 
async def confessionsetup(ctx,channel):
    if channel:
        with open("conf.json", "r") as r:
            conf = json.load(r)
        conf[str(ctx.guild.id)] = channel

        with open("conf.json", "w") as w:
            json.dump(conf, w, indent=4)
        await ctx.send(f'Confession Channel Changed To: {channel}') 
    else:
        await ctx.send("Invalid Channel Or Channel Not Found")


@commands.command(name="ch")
async def ch(ctx,*, message):
    if message:
        with open("conf.json", "r") as r:
            conf = json.load(r) 
        checkchannel = f"<#{ctx.channel.id}>"
        if checkchannel == conf[str(ctx.guild.id)]:
            confession = f"{message}"
            await ctx.message.delete()
            with open('prefixes.json', 'r') as f: 
                prefixes = json.load(f)
            embed = discord.Embed(
                title="",
                description=confession,
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            embed.set_footer(text=f"{prefixes[str(ctx.guild.id)]}ch (message)")
            
            await ctx.send(embed=embed)
        else:
            return
    else:
        await ctx.delete()
        return



