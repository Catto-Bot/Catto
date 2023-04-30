#kadota
import discord
from discord.ext import commands
import random


dice_images = [
   "https://tinyurl.com/yx2zmam4", #dice1
   "https://tinyurl.com/44t66vua", #dice2
   "https://tinyurl.com/mt4xr9pw", #dice3
   "https://tinyurl.com/38hpmpms", #dice4
   "https://tinyurl.com/yy7fmr4f", #dice5
   "https://tinyurl.com/33vt9urr"  # dice 6
]

@commands.command(name="rolldice")
async def rolldice(ctx, member: commands.MemberConverter = None):
    dice_roll = random.randint(1,6)
    dice_roll_image = dice_images[dice_roll-1]
   
    if member:
        dice_roll2 = random.randint(1,6)
        dice_roll2_image = dice_images[dice_roll2-1]
        outcome_msg = f"{ctx.author.name} rolled a {dice_roll}! ({dice_roll_image}) and {member.name} rolled a {dice_roll2}! ({dice_roll2_image})"
        if dice_roll > dice_roll2:
            outcome_msg += f"\n {ctx.author.name} WON!!!"
        elif dice_roll2 > dice_roll:
            outcome_msg += f"\n {member.name} WON!!!"
        else:
            outcome_msg += " \nDRAW!!!"

        embed = discord.Embed(title=f"{ctx.author.name} VS {member.name}", description=outcome_msg, color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title ="DICE ROLL RESULTS",description =f"You rolled a {dice_roll}! ({dice_roll_image})", color=discord.Color.red())
        embed.set_image(url=dice_roll_image)
        embed.set_image(url= dice_roll2_image)
        await ctx.send(embed = embed)

