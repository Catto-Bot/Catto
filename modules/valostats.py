from discord.ext import commands
import discord
import requests
import json
import random
import asyncio



@commands.command(name="vstats")
async def vstats(ctx, name):
    ret = await ctx.send("``Retreiving Data, Please Wait. This May Take Some Time``")
    username,tag = name.split('#')
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}").text
    rankresponse = requests.get(f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{username}/{tag}").text
    valorant_stats = json.loads(response)
    rank_stats = json.loads(rankresponse)
    parse = valorant_stats['data']
    rankparse = rank_stats['data']
    await ret.edit(content="``Almost Done``")
    images = rankparse["images"]
    cards = parse['card']
    embed = discord.Embed(
        title=f"{parse['name']} #{parse['tag']}",
        description=f"Account level: {parse['account_level']}"
    )
    embed.set_image(url=cards["wide"])
    embed.set_footer(text=f"Last Updated: {parse['last_update']} ")
    embed.set_thumbnail(url=images["small"])
    await ret.edit(content="``Found``")
    await ret.edit(embed=embed)
    

@commands.command(name="valofight", aliases=["vf"])
async def valofight(ctx, *, member: discord.Member = None):
    if not member:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        embed = discord.Embed(title="Error!", description="Please mention a user to fight!")
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/4135738/screenshots/13949124/shot-cropped-1596368362081.png")
        embed.set_footer(text=f"The correct format is {prefixes[str(ctx.guild.id)]}valofight")
        await ctx.send(embed=embed)
        return

    agent_pick = {ctx.author.name: "", member.name: ""}
    agent_damage = {ctx.author.name: 150, member.name: 150}

    def checkAuthor(reaction, user):
        return user == ctx.author and reaction.message.id == firstuser.id and str(reaction.emoji) in ["<:jett:1106205144233816164>", "<:raze:1106205146989465660>","<:vandal:1106219261086670859>","<:smoke:1106219255252385923>","<:satchel:1106219252555456602>"]

    def checkMember(reaction, user):
        return user == member and reaction.message.id == firstuser.id and str(reaction.emoji) in ["<:jett:1106205144233816164>", "<:raze:1106205146989465660>","<:vandal:1106219261086670859>","<:smoke:1106219255252385923>","<:satchel:1106219252555456602>"]

    def AuthorWin():
        embed = discord.Embed(title=f"{agent_pick[ctx.author.name]}({ctx.author.name}) Won The Match!", description=f"{agent_pick[ctx.author.name]}({ctx.author.name}): {max(agent_damage[ctx.author.name],0)} HP | {agent_pick[member.name]}({member.name}): {max(agent_damage[member.name],0)} HP")
        return embed
    def MemberWin():
        embed = discord.Embed(title=f"{agent_pick[member.name]}({member.name}) Won The Match!", description=f"{agent_pick[ctx.author.name]}({ctx.author.name}): {max(agent_damage[ctx.author.name],0)} HP | {agent_pick[member.name]}({member.name}): {max(agent_damage[member.name],0)} HP")
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
            deleteraze = await ctx.send("Raze Not Available For Challenger, Full Functionality Coming Soon!")
            await deleteraze.delete(delay=5)
            agent_pick[ctx.author.name] = "Jett"

    except asyncio.TimeoutError:
        await ctx.send("Time Limit Reached")
        return

    try:
        embed = discord.Embed(title="Welcome To Catolant!", description=f"Please Select An Agent {member.name}")
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/4135738/screenshots/13949124/shot-cropped-1596368362081.png")
        embed.add_field(name="", value=f"Challenger:{agent_pick[ctx.author.name]} | Opponent: {agent_pick[member.name]}")
        embed.set_footer(text="Thank You For Using Catto Bot! \nYou Have 20 Seconds To Select An Agent")
        hello = await firstuser.edit(embed=embed)
        await hello.add_reaction("<:jett:1106205144233816164>")
        await hello.add_reaction("<:raze:1106205146989465660>")
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=checkMember)
        if str(reaction.emoji) == "<:jett:1106205144233816164>":
            deleteraze = await ctx.send("Jett Not Available For Challenger, Full Functionality Coming Soon!")
            await deleteraze.delete(delay=5)
            agent_pick[member.name] = "Raze"
        if str(reaction.emoji) == "<:raze:1106205146989465660>":
            agent_pick[member.name] = "Raze"

        embed3 = discord.Embed(title="Welcome To Catolant!", description=f"Please Select An Agent {member.name}")
        embed3.set_thumbnail(url="https://cdn.dribbble.com/users/4135738/screenshots/13949124/shot-cropped-1596368362081.png")
        embed3.add_field(name="", value=f"Challenger: {agent_pick[ctx.author.name]} | Opponent: {agent_pick[member.name]}")
        embed3.set_footer(text="Thank You For Using Catto Bot! \nYou Have 20 Seconds To Select An Agent")
        hello2 = await hello.edit(embed=embed3)
        await hello2.delete()

        def checkJett(reaction, user):
            return user == ctx.author and reaction.message.id == Jett.id and str(reaction.emoji) in ["<:vandal:1106219261086670859>", "<:smoke:1106219255252385923>"]

       

        while agent_damage[ctx.author.name] > 0 or agent_damage[member.name] > 0:
            if agent_pick[ctx.author.name] == "Jett":
                embed = discord.Embed(title=f"{ctx.author.name} vs {member.name}", description=f"Vandal OR Smoke \n{ctx.author.name}'s Turn")
                embed.set_thumbnail(url="https://cdn.oneesports.gg/cdn-data/2021/06/Valorant_JettRetakeCinematic.jpg")
                embed.add_field(name="", value=f"{agent_pick[ctx.author.name]}({ctx.author.name}): {agent_damage[ctx.author.name]} HP | {agent_pick[member.name]}({member.name}): {agent_damage[member.name]} HP")
                embed.set_footer(text="Thank You For Using CattoBot")
                Jett = await ctx.send(embed=embed)
                await Jett.add_reaction("<:vandal:1106219261086670859>")
                await Jett.add_reaction("<:smoke:1106219255252385923>")

                def checkJett(reaction, user):
                    return user == ctx.author and reaction.message.id == Jett.id and str(reaction.emoji) in ["<:vandal:1106219261086670859>", "<:smoke:1106219255252385923>"]
                
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=checkJett)
                if str(reaction.emoji) == "<:vandal:1106219261086670859>":
                    agent_damage[member.name] -= random.randrange(0, 150)
                    
                    if agent_damage[member.name] <= 0:
                        await Jett.delete()
                        await ctx.send(embed=AuthorWin())
                        return
                if str(reaction.emoji) == "<:smoke:1106219255252385923>":
                    await Jett.delete()
                    embed=discord.Embed(title="",description=f"You Used Your Smoke To Run Away From {member.name}")
                    embed.add_field(name=f"{member.name} Won!", value="")
                    await ctx.send(embed=embed)
                    return
                
            #if agent_pick[ctx.author.name] == "Raze":
                #await ctx.send("Please, Select Jett\nFull Functionality Coming Soon!")
                #continue

            #if agent_pick[member.name] == "Jett":
                #await ctx.send("Please, Select Raze\nFull Functionality Coming Soon!")
                #continue
            

            if agent_pick[member.name] == "Raze":
                embed2 = discord.Embed(title=f"{ctx.author.name} vs {member.name}", description=f"Vandal OR Satchel \n{member.name}'s Turn")
                embed2.set_thumbnail(url="https://www.nme.com/wp-content/uploads/2020/07/072220-Raze-Valorant-Riot-Games.jpg")
                embed2.add_field(name="", value=f"{agent_pick[ctx.author.name]}({ctx.author.name}): {agent_damage[ctx.author.name]} HP | {agent_pick[member.name]}({member.name}): {agent_damage[member.name]} HP")
                embed2.set_footer(text="Thank You For Using CattoBot")
                await Jett.clear_reactions()
                Jettembed = await Jett.edit(embed=embed2)
                await Jettembed.add_reaction("<:vandal:1106219261086670859>")
                await Jettembed.add_reaction("<:satchel:1106219252555456602>")

                def checkRaze(reaction, user):
                    return user == member and reaction.message.id == Jettembed.id and str(reaction.emoji) in ["<:vandal:1106219261086670859>", "<:satchel:1106219252555456602>"]
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=checkRaze)

                if str(reaction.emoji) == "<:vandal:1106219261086670859>":
                    agent_damage[ctx.author.name] -= random.randrange(0, 150)
                    if agent_damage[ctx.author.name] <= 0:
                        await Jettembed.delete()
                        await ctx.send(embed=MemberWin())
                        return
                if str(reaction.emoji) == "<:satchel:1106219252555456602>":
                    await Jettembed.delete()
                    embed=discord.Embed(title="",description=f"You Used Your Satchel To Run Away From {ctx.author.name}")
                    embed.add_field(name=f"{ctx.author.name} Won!", value="")
                    await ctx.send(embed=embed)
                    return
                await Jettembed.delete()
            
        
    except Exception as e:
        await ctx.send(e)


@valofight.error
async def valofight_error(ctx,error):
    await ctx.send("Time limit Reached!")
    print(error)

@vstats.error
async def vstats_error(ctx, err):
    print(err)
    with open('prefixes.json', 'r') as f: 

        prefixes = json.load(f)
    embed= discord.Embed(title="Error!", description=f"Error While Retrieving Data. Please Try Again Later")
    embed.add_field(inline=False, name="Format", value=f"The Correct Format is {prefixes[str(ctx.guild.id)]}vstats (username#tagline)")
    embed.set_footer(text="Thank You For Using Catto!")
    await ctx.send(embed=embed)








    
