#aryn
from discord.ext import commands

@commands.command(name="meme")
async def meme(ctx):
    await ctx.channel.send("You are the meme hehehe!")
    await ctx.channel.send("omg!")

