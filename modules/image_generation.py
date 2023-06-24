from discord.ext import commands
import discord
import requests
import io
import os
from PIL import Image
import time
from dotenv import load_dotenv
import asyncio

load_dotenv()

HUGGING_FACE_KEY= os.getenv('HUGGING_FACE_KEY')
HUGGING_FACE_PRIVATE_KEY= os.getenv('HUGGING_FACE_PRIVATE_KEY')

def save(ctx, msg):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author} Prompt: {msg}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author} Prompt: {msg}")
allowed_users = []  


@commands.command(name="aiterms")
async def aiterms(ctx):
    try:
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == verify.id and str(reaction.emoji) in ["✅", "❌"]
        
        # Check if user already has access
        with open("ai_allowed.txt", "r") as file:
            allowed_users = file.read().splitlines()
            if str(ctx.author.id) in allowed_users:
                await ctx.send(f"``{ctx.author.name}, you already have access.``")
                return
        
        embed = discord.Embed(title="Terms and Conditions")
        embed.add_field(name="Prohibited Content", value="The generation of explicit or NSFW images is strictly prohibited. Users found generating or sharing such content will be subject to immediate PERMANENT ban.")

        embed.add_field(name="Command Usage", value="Please refrain from spamming the image generation command excessively. Excessive use may result in limitations or cooldowns to ensure fair usage for all users.")

        embed.add_field(name="User Responsibility", value="By using the ai command, you acknowledge and agree that you are solely responsible for the images generated and their usage. The bot owner and developers hold no liability for any content generated or its consequences.")

        embed.add_field(name="Vote", value="Also, make sure to vote for the bot [here](https://top.gg/bot/1108380972950491146).")

        embed.set_footer(text="By using the image generation command, you agree to abide by these terms and conditions.")
        verify = await ctx.send(embed=embed)
        await verify.add_reaction("✅")
        await verify.add_reaction("❌")
        
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=check)
            if str(reaction.emoji) == "✅":
                try:
                    with open("ai_allowed.txt", "a") as file:
                        file.write(str(ctx.author.id) + "\n")
                    await verify.edit(content = f"``Access granted to {ctx.author.name}.``")
                    await verify.clear_reactions()
                except Exception as err:
                    await ctx.send(f"Error occurred: {err}")
                    await verify.clear_reactions()

            if str(reaction.emoji) == "❌":
                await verify.edit(content = "``Aborted.``")
                await verify.clear_reactions()
                return
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Expired", description="")
            await verify.edit(embed=embed)
            await verify.clear_reactions()
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        await verify.clear_reactions()



# @commands.command(name="addai")
# @commands.check(lambda ctx: ctx.author.id == 780639741866409984)
# async def addai(ctx, msg):
#     try:
#         with open("ai_allowed.txt", "a") as file:
#             file.write(msg + "\n")
#         await ctx.send("done")
#     except Exception as err:
#         await ctx.send(err)

@commands.command(name="ai")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ai(ctx, *, msg):
    if msg:
        save(ctx, msg)
        try:
            with open("ai_allowed.txt", "r") as read:
                allowed_users = read.readlines()
            allowed_users = [int(user_id.strip()) for user_id in allowed_users]  
            if ctx.author.id not in allowed_users:
                embed = discord.Embed(title="Error", description=f"Hi {ctx.author.name}, use ``!aiterms`` first to be authorized ")
                embed.set_footer(text="Support Server: https://discord.gg/cvNa9XTbD9")
                await ctx.send(embed=embed)
                return
            
        
            if ai.locked:
                await ctx.reply(f"Hi {ctx.author.name} , The command is currently being used by someone else. Please wait for it to be available.")
                return

            ai.locked = True
            ret = await ctx.send("Generating Image <a:loading:1108012790783946772>")
            
            API_URL = "https://api-inference.huggingface.co/models/NoCrypt/SomethingV2_2"
            headers = {"Authorization": HUGGING_FACE_KEY}
    
            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.content

            image_bytes = query({
                "inputs": msg,
            })

            image = Image.open(io.BytesIO(image_bytes))

            image.save("output.png")

            with open('output.png', 'rb') as f:
                picture = discord.File(f)
                embed = discord.Embed(title="Generated Image", description=f"Prompt: {msg}", color=0x000000)
                embed.set_image(url="attachment://output.png")
                embed.set_footer(text="Note: Generating Explicit Images Will Result In A Ban")
                await ret.delete()
                await ctx.reply(embed=embed, file=picture)
                
        except Exception as err:
            await ctx.send(err)

        finally:
            ai.locked = False
            os.remove('output.png')
    else:
        await ctx.send("``Please Enter A Prompt!``")


# Cooldown error handler
@ai.error
async def ai_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after)
        await ctx.send(f"This command is on cooldown. Please try again in {remaining} second(s).")
    else:
         await ctx.send("``Please Enter A Prompt!``")

    



ai.locked = False


lock = asyncio.Lock()
@commands.command(name="privai")
@commands.check(lambda ctx: ctx.author.id == 780639741866409984 or ctx.author.id == 839691122481299506 or ctx.author.id == 534977801116319745 or ctx.author.id == 540405934367703050 or ctx.author.id == 582506141959979008 or ctx.author.id == 374959702242754560 or ctx.author.id == 851012067552788511 or ctx.author.id == 588025801455304707)
@commands.cooldown(1, 15, commands.BucketType.user)
async def privai(ctx, *, msg):
    # Acquire the lock
    async with lock:
        save(ctx, msg)

        try:
            hello = await ctx.send("Loading..")
            API_URL = "https://api-inference.huggingface.co/models/AIARTCHAN/AbyssMapleVer3"
            headers = {"Authorization": HUGGING_FACE_PRIVATE_KEY}

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.content

            image_bytes = query({
                "inputs": msg,
            })

            image = Image.open(io.BytesIO(image_bytes))

            image.save("output2.png")

            with open('output2.png', 'rb') as f:
                picture = discord.File(f)
                embed = discord.Embed(title="Generated Image", description=f"Prompt: {msg}", color=0x000000)
                embed.set_image(url="attachment://output2.png")
                embed.set_footer(text="Note: Generating Explicit Images Will Result In A Ban")
                await hello.delete()
                await ctx.reply(embed=embed, file=picture)

        except Exception as err:
            await ctx.send(err)

        finally:
            os.remove('output2.png')



# Cooldown error handler
@privai.error
async def privai_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after)
        await ctx.send(f"This command is on cooldown. Please try again in {remaining} second(s).")
    


