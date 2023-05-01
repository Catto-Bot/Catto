#kadota
import discord
from discord.ext import commands
import random
import aiohttp
import io

# dice_images = [
#    "https://tinyurl.com/yx2zmam4", #dice1
#    "https://tinyurl.com/44t66vua", #dice2
#    "https://tinyurl.com/mt4xr9pw", #dice3
#    "https://tinyurl.com/mry42pe6", #dice4
#    "https://tinyurl.com/yy7fmr4f", #dice5
#    "https://tinyurl.com/33vt9urr"  # dice 6
# ]
dice_images = [
   "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Dice-1-b.svg/1024px-Dice-1-b.svg.png", #dice1
   "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Dice-2-b.svg/1200px-Dice-2-b.svg.png", #dice2
   "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Dice-3-b.svg/1200px-Dice-3-b.svg.png", #dice3
   "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Dice-4-b.svg/557px-Dice-4-b.svg.png", #dice4
   "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Dice-5-b.svg/2048px-Dice-5-b.svg.png", #dice5
   "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Dice-6-b.svg/768px-Dice-6-b.svg.png"  # dice 6
]


@commands.command(name="rolldice")
async def rolldice(ctx, member: commands.MemberConverter = None):
    dice_roll = random.randint(1,6)
    dice_roll2 = random.randint(1,6)
    dice_img_url = dice_images[dice_roll-1] # get corresponding dice image URL based on dice roll
    if member:
         # get corresponding dice image URL based on dice roll
        outcome_msg = f"{ctx.author.name} rolled a {dice_roll}! and {member.name} rolled a {dice_roll2}!"
        embed1 = discord.Embed(title=f"{ctx.author.name}\tVS\t{member.name}",description=outcome_msg, color=0x333333)
        if dice_roll>dice_roll2:
            embed1.set_footer(text=f"Winner:{ctx.author.name}🏆")
        elif dice_roll2 > dice_roll:
            embed1.set_footer(text=f"Winner: {member.name}🏆")
        else:
            embed1.set_footer(text="DRAW!!!")
            embed1.set_thumbnail(url=dice_img_url)
        # embed1.set_footer(text=outcome_msg)
        await ctx.send(embed =embed1)    
          
    else:
        embed = discord.Embed(title ="DICE ROLL RESULTS",description =f"You rolled a {dice_roll}! ", color=0x333333)
        embed.set_thumbnail(url=dice_img_url)
        await ctx.send(embed = embed)
