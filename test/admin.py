from discord.ext import commands
import discord
import time

@commands.command(name="test")
async def test(ctx):
    allowed_users = [780639741866409984, 582506141959979008,540405934367703050,534977801116319745]  # Replace with the actual user IDs allowed to use the command
    if ctx.author.id not in allowed_users:
        await ctx.send("Sorry, this command can only be used by certain people.")
        return
    firsttime = time.time()/1000
    await ctx.send(f"{time.time()/1000 - firsttime}")

    