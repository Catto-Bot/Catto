import discord
from discord.ext import commands
import random

def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
@commands.command(name="ship")
async def ship(ctx, *, member: discord.Member = None):
    save(ctx)
    if member:
        if len(ctx.message.mentions) == 0:
            await ctx.send("Please mention a user to ship!")
            return
        
        mentioned_user = ctx.message.mentions[0]
        hellohi = mentioned_user.display_name
        user = ctx.message.author.display_name
        shippercen = str(random.randint(0, 100))
        
        embed = discord.Embed(
            title="❤️ **MATCHMAKING** ❤️",
            color=0xFF69B4
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name=user, value="🔻", inline=True)
        embed.add_field(name="💖💖", value="{}%".format(shippercen), inline=True)
        embed.add_field(name=hellohi, value="🔻", inline=True)
        
        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("Please Mention A User")

