#ghost
import discord
from discord.ext import commands
import requests
import json
import html
import asyncio

API_KEY ='aEIxt6NSkJGib80neq+dRg==p1ytbEYfgbfg9zBW'


##############################################################################################
# Some Worthy Quotes
##############################################################################################

@commands.command(name="quote")
async def quote(ctx):
    try:
        api_url = 'https://api.quotable.io/random'
        
        response = requests.get(api_url)
        data = response.json()
        quotes = data['content']
        author = data['author']
        category = data['tags'][0]
        embed = discord.Embed(title=f"{category}", description=f"\"{quotes}\"", color=0x777777)
        embed.set_footer(text=f"-{author}")
        quote = await ctx.channel.send(embed=embed)
        await quote.add_reaction("👍")
        await quote.add_reaction("👎")
        
    except:
        await ctx.channel.send(f"I am down myself 🥲")

########################################################################################################################
# DEV JOKE
########################################################################################################################

@commands.command(name="devjoke")
async def devjoke(ctx):
    try:
        api_url= "https://backend-omega-seven.vercel.app/api/getjoke"
        response  = requests.get(api_url)
        data = response.json()[0]
        question = data['question']
        punchline = data['punchline']
        embed = discord.Embed(title=f'{question}', color=0x555555)
        devjoke = await ctx.channel.send(embed = embed)

        await asyncio.sleep(5)

        embed = discord.Embed(title=f"{question} \n {punchline}", color=0x666666)
        devjoke = await devjoke.edit(embed = embed)
        await devjoke.add_reaction("👍")
        await devjoke.add_reaction("👎")

    except Exception as err:
        print(err)



################################################################################################
# Trivia #
################################################################################################
@commands.command(name = "trivia")
async def trivia(ctx):
        api_url ="https://opentdb.com/api.php?amount=1&type=boolean"
        d = json.loads(
        requests.get(api_url).text
        )
        data = d['results'][0]
        category =data['category']
        difficulty =data['difficulty']
        question = html.unescape(data['question'])
        correct_ans = data['correct_answer']
        ans={}
        if(correct_ans == "True"):
            ans = {'correct': '🟩'}
        if(correct_ans == "False"):
            ans = {'correct': '❌'}
        embed = discord.Embed(title=f"{question}", description=f"{category}({difficulty.capitalize()})", color=0x333333)
        trivia = await ctx.channel.send(embed = embed)
        await trivia.add_reaction("🟩")
        await trivia.add_reaction("❌")

        def check(reaction, user):
            return (
                user != ctx.bot.user
                and reaction.message.id == trivia.id
                and str(reaction.emoji) in ["🟩", "❌"]
            )

        try:
            reaction, user = await ctx.bot.wait_for(
                "reaction_add", timeout=20.0, check=check
            )
            if str(reaction.emoji) == ans['correct']:
                embed = discord.Embed(description=f"{user.mention} was right", color=0x00ff00)
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(description=f"{user.mention} was wrong", color=0xff0000)
                await ctx.send(embed = embed)

            await asyncio.sleep(10)

            await trivia.delete()
        except:
            embed = discord.Embed(title='Nobody reacted in time 😔', color=0xff0000)
            await ctx.send(embed = embed)
            await trivia.delete()



######################################################################################################
# Dad joke #
######################################################################################################
@commands.command(name = "dadjoke")
async def dadjoke(ctx):
    try:
        api_url = 'https://icanhazdadjoke.com/slack'
        response = requests.get(api_url)
        d = response.json()
       
        daddy=d['attachments'][0]['fallback']

        embed = discord.Embed(title=f'{daddy}', color=0x555555)
        await ctx.send(embed = embed)
    except:
        await ctx.channel.send("My dad left me like your left to buy milk 😁")


####################################################################################
#Insult
####################################################################################
@commands.command(nmae ="insult")
async def insult(ctx):
        try: 
            api_url= 'https://evilinsult.com/generate_insult.php?lang=en&type=json'
            response = requests.get(api_url)
            d = response.json()
            insult = html.unescape(d['insult'])
            embed = discord.Embed(title=f'{insult}', color=0x555555)
            print(d)
            await ctx.send(embed = embed)
        except Exception as err:
            print(err)


#####################################################################
#Dark Meme
#####################################################################
@commands.command()
async def darkmeme(ctx):
        try: 
            api_url= f'https://v2.jokeapi.dev/joke/Dark?type=twopart'
            response = requests.get(api_url)
            d = response.json()
            setup = html.unescape(d["setup"])
            delivery = html.unescape(d["delivery"])
            embed = discord.Embed(title=f'{setup}', color=0x555555)
            darkjoke = await ctx.channel.send(embed = embed)

            await asyncio.sleep(3)

            embed = discord.Embed(title=f"{setup} \n {delivery}", color=0x666666)
            darkjoke = await darkjoke.edit(embed = embed)
            await darkjoke.add_reaction("👍")
            await darkjoke.add_reaction("👎")
            
        except Exception as err:
            print(err)


######################################################################
# Spooky
######################################################################

@commands.command(name ="spooky")
async def spooky(ctx):
        try: 
            api_url= f'https://v2.jokeapi.dev/joke/Spooky?type=twopart'
            response = requests.get(api_url)
            d = response.json()
            setup = html.unescape(d["setup"])
            delivery = html.unescape(d["delivery"])
            embed = discord.Embed(title=f'{setup}', color=0x555555)
            darkjoke = await ctx.channel.send(embed = embed)

            await asyncio.sleep(3)

            embed = discord.Embed(title=f"{setup} \n {delivery}", color=0x666666)
            darkjoke = await darkjoke.edit(embed = embed)
            await darkjoke.add_reaction("👍")
            await darkjoke.add_reaction("👎")
            
        except Exception as err:
            print(err)

######################################################################
# Advice
######################################################################

@commands.command(name ="advice")
async def spooky(ctx):
        try: 
            api_url= f'https://api.adviceslip.com/advice'
            response = requests.get(api_url)
            d = response.json()
            setup = html.unescape(d["slip"]["advice"])
            embed = discord.Embed(title=f'{setup}', color=0x555555)
            await ctx.channel.send(embed = embed)
            
        except Exception as err:
            print(err)
