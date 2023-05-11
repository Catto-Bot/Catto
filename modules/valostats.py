from discord.ext import commands
import discord
import requests
import json
import random

@commands.command(name="maps")
async def maps(ctx):
    response = requests.get('https://valorant-api.com/v1/maps')
    json_data = response.json()

    display_names = []

    for map_data in json_data['data']:
        if 'displayName' in map_data and map_data['displayName']:
            display_names.append(map_data['displayName'])

    random = await ctx.send(display_names)
    await random.delete()


@commands.command(name="vstats")
async def vstats(ctx, name):
    username,tag = name.split('#')
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}").text
    rankresponse = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{username}/{tag}").text
    valorant_stats = json.loads(response)
    rank_stats = json.loads(rankresponse)
    parse = valorant_stats['data']
    rankparse = rank_stats['data']
    images = rankparse["images"]
    cards = parse['card']
    embed = discord.Embed(
        title=f"{parse['name']} #{parse['tag']}",
        description=f"Account level: {parse['account_level']}"
    )
    embed.set_image(url=cards["wide"])
    embed.set_footer(text=f"Last Updated: {parse['last_update']} ")
    embed.set_thumbnail(url=images["small"])
    await ctx.send(embed=embed)

@commands.command(name="valofight", aliases=["vf"])
async def valofight(ctx, *, member: discord.Member = None):
    if not member:
        with open('prefixes.json', 'r') as f: 
            prefixes = json.load(f)
        embed = discord.Embed(title="Error!", description="Please Mention A User To Mention!")
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/4135738/screenshots/13949124/shot-cropped-1596368362081.png")
        embed.set_footer(text=f"The Correct Format is {prefixes[str(ctx.guild.id)]}valofight")
        await ctx.send(embed=embed)
        
    if member:
            agent_pick = {ctx.author.name: "", member.name: ""}
            agent_damage = {ctx.author.name: 150, member.name: 150}

            def checkAuthor(reaction, user):
                return user == ctx.author and reaction.message.id == firstuser.id and str(reaction.emoji) in ["<:jett:1106205144233816164>", "<:raze:1106205146989465660>","<:vandal:1106219261086670859>","<:smoke:1106219255252385923>","<:satchel:1106219252555456602>"]
            
            def checkMember(reaction, user):
                return user == member and reaction.message.id == firstuser.id and str(reaction.emoji) in ["<:jett:1106205144233816164>", "<:raze:1106205146989465660>","<:vandal:1106219261086670859>","<:smoke:1106219255252385923>","<:satchel:1106219252555456602>"]
            
            def Dead():
                embed = discord.Embed(title=f"{agent_pick[ctx.author.name]}({ctx.author.mention}) Won The Match!", description="")
                return embed

            embed = discord.Embed(title="Welcome To Catolant!", description=f"Please Select An Agent {ctx.author.name}")
            embed.set_thumbnail(url="https://cdn.dribbble.com/users/4135738/screenshots/13949124/shot-cropped-1596368362081.png")
            embed.set_footer(text="Thank You For Using Catto Bot! \nYou Have 20 Seconds To Select An Agent")
            firstuser = await ctx.send(embed=embed)
            await firstuser.add_reaction("<:jett:1106205144233816164>")
            await firstuser.add_reaction("<:raze:1106205146989465660>")
            
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=checkAuthor)
                if str(reaction.emoji) == "<:jett:1106205144233816164>":
                    agent_pick[ctx.author.name] = "Jett"
                if str(reaction.emoji) == "<:raze:1106205146989465660>":
                    agent_pick[ctx.author.name] = "raze"

            except:
                print(err)
                await ctx.send("Time Limit Reached")
                return
            
            try:
                embed = discord.Embed(title="Welcome To Catolant!", description=f"Please Select An Agent {member.name}")
                embed.set_thumbnail(url="https://cdn.dribbble.com/users/4135738/screenshots/13949124/shot-cropped-1596368362081.png")
                embed.add_field(name="", value=f"Challenger: {agent_pick[ctx.author.name]} | Opponent: {agent_pick[member.name]}")
                embed.set_footer(text="Thank You For Using Catto Bot! \nYou Have 20 Seconds To Select An Agent")
                hello = await firstuser.edit(embed=embed)
                await firstuser.add_reaction("<:jett:1106205144233816164>")
                await firstuser.add_reaction("<:raze:1106205146989465660>")
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=checkMember)
                if str(reaction.emoji) == "<:jett:1106205144233816164>":
                    agent_pick[member.name] = "Jett"
                if str(reaction.emoji) == "<:raze:1106205146989465660>":
                    agent_pick[member.name] = "raze"

                embed3 = discord.Embed(title="Welcome To Catolant!", description=f"Please Select An Agent {member.name}")
                embed3.set_thumbnail(url="https://cdn.dribbble.com/users/4135738/screenshots/13949124/shot-cropped-1596368362081.png")
                embed3.add_field(name="", value=f"Challenger: {agent_pick[ctx.author.name]} | Opponent: {agent_pick[member.name]}")
                embed3.set_footer(text="Thank You For Using Catto Bot! \nYou Have 20 Seconds To Select An Agent")
                hello2 = await hello.edit(embed=embed3)
            except Exception as err:
                print(err)
                await ctx.send("Time Limit Reached")
                return

            await hello2.delete()
            if agent_pick[ctx.author.name] == "Jett":
                embed = discord.Embed(title=f"{ctx.author.name} vs {member.name}", description="Vandal OR Smoke")
                embed.set_thumbnail(url="https://cdn.oneesports.gg/cdn-data/2021/06/Valorant_JettRetakeCinematic.jpg")
                embed.set_footer(text="Thank You For Using CattoBot")
                Jett = await ctx.send(embed=embed)
                await Jett.add_reaction("<:vandal:1106219261086670859>")
                await Jett.add_reaction("<:smoke:1106219255252385923>") 
                
                def checkJett(reaction, user):
                    return user == ctx.author and reaction.message.id == Jett.id and str(reaction.emoji) in ["<:vandal:1106219261086670859>","<:smoke:1106219255252385923>"]
                
                def checkRaze(reaction, user):
                    return user == ctx.author and reaction.message.id == Jett.id and str(reaction.emoji) in ["<:vandal:1106219261086670859>","<:satchel:1106219252555456602>"]
                
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=checkJett)
                if str(reaction.emoji) == "<:vandal:1106219261086670859>":
                    agent_damage[member.name] = agent_damage[member.name] - random.randrange(1,150)
                    if agent_damage[member.name] <= 0:
                        await ctx.send(embed=Dead())
                        return
                    else:
                        if agent_pick[member.name] == "Raze":
                            embed2 = discord.Embed(title=f"{ctx.author.name} vs {member.name}", description="Vandal OR Satchel")
                            embed2.set_thumbnail(url="https://www.nme.com/wp-content/uploads/2020/07/072220-Raze-Valorant-Riot-Games.jpg")
                            embed2.add_field(name="", value=f"{agent_pick[ctx.author.name]}({ctx.author.name}): {agent_damage[ctx.author.name]} HP | {agent_pick[member.name]}({member.name}): {agent_damage[member.name]} HP")
                            embed2.set_footer(text="Thank You For Using CattoBot")
                            Razeembed = await Jett.edit(embed=embed2)
                            await Razeembed.add_reaction("<:vandal:1106219261086670859>")
                            await Razeembed.add_reaction("<:satchel:1106219252555456602>") 

                        if agent_pick[member.name] == "Jett":
                            embed2 = discord.Embed(title=f"{ctx.author.name} vs {member.name}", description="Vandal OR Smoke")
                            embed2.set_thumbnail(url="https://cdn.oneesports.gg/cdn-data/2021/06/Valorant_JettRetakeCinematic.jpg")
                            embed2.add_field(name="", value=f"{agent_pick[ctx.author.name]}({ctx.author.name}): {agent_damage[ctx.author.name]} HP | {agent_pick[member.name]}({member.name}): {agent_damage[member.name]} HP")
                            embed2.set_footer(text="Thank You For Using CattoBot")
                            Jettembed = await Jett.edit(embed=embed2)
                            await Jettembed.add_reaction("<:vandal:1106219261086670859>")
                            await Jettembed.add_reaction("<:smoke:1106219255252385923>") 

            #await ctx.send(f"{agent_pick[ctx.author.name]}")
            #await ctx.send(f"{agent_pick[member.name]}")



@valofight.error
async def valofight_error(ctx,error):
    await ctx.send("An error occured!")
    print(error)

@vstats.error
async def vstats_error(ctx,name):
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)
    embed= discord.Embed(title="Error!", description=f"Error While Retrieving Data. Please Try Again Later")
    embed.add_field(inline=False, name="Format", value=f"The Correct Format is {prefixes[str(ctx.guild.id)]}vstats (username#tagline)")
    embed.set_footer(text="Thank You For Using Catto!")
    await ctx.send(embed=embed)








    
