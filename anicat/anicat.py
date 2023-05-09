from discord.ext import commands
import discord
import json
import random


# Print names
@commands.command()
async def anime(ctx):
    with open("data.json", "r", encoding="utf8") as file:
        data = json.load(file)

# Extract names
    names = [item["Name"] for item in data]
    source = [item["Source"] for item in data]
    points = [item["Points"] for item in data]
    random_index = random.randint(0, len(names) - 1)
    embed = discord.Embed(title=f"{names[random_index]}", description="")
    embed.set_image(url=source[random_index])
    embed.set_footer(text=f"You Gained A Total Of {points[random_index]} Points!")

    await ctx.send(embed=embed)
