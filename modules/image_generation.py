from discord.ext import commands
import discord
import requests
import io
import os
from PIL import Image
import time
from dotenv import load_dotenv

load_dotenv()

HUGGING_FACE_KEY= os.getenv('HUGGING_FACE_KEY')

def save(ctx, msg):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author} Prompt: {msg}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author} Prompt: {msg}")
allowed_users = []  


@commands.command(name="ai")
@commands.cooldown(5, 60, commands.BucketType.user)
async def ai(ctx, *, msg):
    save(ctx, msg)
    try:
        with open("ai_allowed.txt", "r") as read:
            allowed_users = read.readlines()
        allowed_users = [int(user_id.strip()) for user_id in allowed_users]  
        if ctx.author.id not in allowed_users:
            embed = discord.Embed(title="Error", description=f"Hi {ctx.author.name}, You are not authorized to use this command.")
            embed.set_footer(text="Support Server: https://discord.gg/rvQXeuMwdG")
            await ctx.send(embed=embed)
            return
        
       
        if ai.locked:
            await ctx.reply(f"Hi {ctx.author.name} , The command is currently being used by someone else. Please wait for it to be available.")
            return

        ai.locked = True
        ret = await ctx.send("Generating Image <a:loading:1108012790783946772>")
        
        API_URL = "https://api-inference.huggingface.co/models/andite/anything-v4.0"
        headers = {"Authorization": HUGGING_FACE_KEY}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.content

        image_bytes = query({
            "inputs": msg,
        })

        image = Image.open(io.BytesIO(image_bytes))

        image.save("output.jpg")

        with open('output.jpg', 'rb') as f:
            picture = discord.File(f)
            embed = discord.Embed(title="Generated Image", description=f"Prompt: {msg}", color=0x000000)
            embed.set_image(url="attachment://output.jpg")
            embed.set_footer(text="Note: Generating Explicit Images Will Result In A Ban")
            await ret.delete()
            await ctx.reply(embed=embed, file=picture)
            
    except Exception as err:
        await ctx.send(err)

    finally:
        ai.locked = False
        os.remove('output.jpg')


# Cooldown error handler
@ai.error
async def ai_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after)
        await ctx.send(f"This command is on cooldown. Please try again in {remaining} second(s).")



ai.locked = False