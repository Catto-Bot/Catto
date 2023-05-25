from discord.ext import commands
import discord
import json
import random
import asyncio
import time

def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")

cooldown_time = 1 * 60 * 60
@commands.command(name="anicat", aliases=["ac","anic"])
@commands.cooldown(20, cooldown_time, commands.BucketType.user)
async def anicat(ctx):
    save(ctx)
    
    with open("data/data.json", "r", encoding="utf8") as file:
        data = json.load(file)

    names = [item["Name"] for item in data]
    source = [item["Source"] for item in data]
    points = [item["Points"] for item in data]
    random_index = random.randint(0, len(names) - 1)
    embed = discord.Embed(title=f"{names[random_index]}", description="")
    embed.set_image(url=source[random_index])
    embed.set_footer(text=f"Points: {points[random_index]} \nPress On The Emoji To Claim")

    final = await ctx.send(embed=embed)
    await final.add_reaction("<:anicat:1105722682160447550>")

    def check(reaction, user):
        return reaction.message.id == final.id and user != ctx.bot and str(reaction.emoji) in ["<:anicat:1105722682160447550>"]

    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.00, check=check)

        if str(reaction.emoji) == "<:anicat:1105722682160447550>":
            embed = discord.Embed(title=f"claimed by {user}", description="")
            embed.set_image(url=source[random_index])
            embed.set_footer(text=f"Thank You For Using Catto Bot(Anicat)")
            embed.set_author(name=names[random_index])
            await final.edit(embed=embed)
            await final.clear_reactions()
            user_name = str(user)
            try:
                with open("data/anicat.json", "r", encoding="utf8") as file:
                    anicatdata = json.load(file)
            except:
                anicatdata = {}

            if user_name in anicatdata:
                anicatdata[user_name]["Total AniCats"] += 1
                anicatdata[user_name]["Total AniPoints"] += points[random_index]
                if names[random_index] not in anicatdata[user_name]["Names"]:
                    anicatdata[user_name]["Names"].append(names[random_index])  # Add the name to the list
            else:
                anicatdata[user_name] = {
                    "Total AniCats": 1,
                    "Total AniPoints": points[random_index],
                    "Names": [names[random_index]]  # Create a list with the name
            }


            with open("data/anicat.json", "w") as final:
                json.dump(anicatdata, final)

    except Exception as e:
        editembed = discord.Embed(title="Expired!", description="You Took Too Long To Claim!")
        editembed.set_image(url=source[random_index])
        editembed.set_footer(text=f"Thank You For Using Catto Bot(Anicat)")
        await final.clear_reactions()
        await final.edit(embed=editembed)
        return



@commands.command(name="anicatstats", aliases=["as", "stats"])
async def anicatstats(ctx, *, member: discord.Member = None):
    save(ctx)
    page = 1
    starting = 0
    ending = 10
    try:
        with open("data/anicat.json", "r", encoding="utf8") as file:
            anicatdata = json.load(file)

        if member:
            member_name = str(member)
            if member_name in anicatdata:
                total_anicats = anicatdata[member_name]["Total AniCats"]
                total_anipoints = anicatdata[member_name]["Total AniPoints"]
                names = anicatdata[member_name]["Names"]

                embed = discord.Embed(title=f"Anicat Info for {member_name}", description="", color=discord.Color.green())
                embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                embed.add_field(name="Anicats Info", value="\n".join(names[starting:ending]), inline=False)
                embed.set_footer(text=f"Page: {page}")

                anothercheck = await ctx.send(embed=embed)
                await anothercheck.add_reaction("⬅️")
                await anothercheck.add_reaction("➡️")

                def check(reaction, user):
                    return user == ctx.author and reaction.message.id == anothercheck.id and str(reaction.emoji) in ["⬅️", "➡️"]

                timer_seconds = 60
                end_time = time.time() + timer_seconds
                while time.time() < end_time:
                    try:
                        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=end_time - time.time(), check=check)
                        if str(reaction.emoji) == "➡️":
                            page += 1
                            starting += 10
                            ending += 10
                            embed = discord.Embed(title=f"Anicat Info for {member_name}", description="", color=discord.Color.green())
                            embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                            embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                            embed.add_field(name="Anicats Info", value="\n".join(names[starting:ending]), inline=False)
                            embed.set_footer(text=f"Page: {page}")
                            await anothercheck.edit(embed=embed)
                            await anothercheck.remove_reaction(reaction, user)

                        if str(reaction.emoji) == "⬅️":
                            if page > 1:
                                page -= 1
                                starting -= 10
                                ending -= 10
                                embed = discord.Embed(title=f"Anicat Info for {member_name}", description="", color=discord.Color.green())
                                embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                                embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                                embed.add_field(name="Anicats Info", value="\n".join(names[starting:ending]), inline=False)
                                embed.set_footer(text=f"Page: {page}")
                                await anothercheck.edit(embed=embed)
                                await anothercheck.remove_reaction(reaction, user)
                            else:
                                await anothercheck.edit(content="``You are already on the first page.``")

                    except asyncio.TimeoutError:
                        break

            else:
                await ctx.send("No Record Found")
        else:
            author_name = str(ctx.author)
            if author_name in anicatdata:
                total_anicats = anicatdata[author_name]["Total AniCats"]
                total_anipoints = anicatdata[author_name]["Total AniPoints"]
                names = anicatdata[author_name]["Names"]

                embed = discord.Embed(title=f"Anicat Info for {author_name}", description="", color=discord.Color.magenta())
                embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                embed.add_field(name="Anicats Info", value="\n".join(names[starting:ending]), inline=False)
                embed.set_footer(text=f"Page: {page}")

                owncheck = await ctx.send(embed=embed)
                await owncheck.add_reaction("⬅️")
                await owncheck.add_reaction("➡️")

                def check(reaction, user):
                    return user == ctx.author and reaction.message.id == owncheck.id and str(reaction.emoji) in ["⬅️", "➡️"]

                timer_seconds = 60
                end_time = time.time() + timer_seconds
                while time.time() < end_time:
                    try:
                        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=end_time - time.time(), check=check)
                        if str(reaction.emoji) == "➡️":
                            page += 1
                            starting += 10
                            ending += 10
                            embed = discord.Embed(title=f"Anicat Info for {author_name}", description="", color=discord.Color.magenta())
                            embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                            embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                            embed.add_field(name="Anicats Info", value="\n".join(names[starting:ending]), inline=False)
                            embed.set_footer(text=f"Page: {page}")
                            await owncheck.edit(embed=embed)
                            await owncheck.remove_reaction(reaction, user)

                        if str(reaction.emoji) == "⬅️":
                            if page > 1:
                                page -= 1
                                starting -= 10
                                ending -= 10
                                embed = discord.Embed(title=f"Anicat Info for {author_name}", description="", color=discord.Color.magenta())
                                embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                                embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                                embed.add_field(name="Anicats Info", value="\n".join(names[starting:ending]), inline=False)
                                embed.set_footer(text=f"Page: {page}")
                                await owncheck.edit(embed=embed)
                                await owncheck.remove_reaction(reaction, user)
                            else:
                                await owncheck.edit(content="``You are already on the first page.``")

                    except asyncio.TimeoutError:
                        break

            else:
                await ctx.send("No record found!")
                return
    except Exception as err:
        await ctx.send(str(err))
        return





@commands.command("anicatinfo", aliases=["aci"])
async def anicatinfo(ctx, *,card):
    save(ctx)
    try:
        with open("data/data.json", "r") as read:
            data = json.load(read)

        card_lower = card.lower()
        matching_items = [item for item in data if card_lower in item["Name"].lower()]

        if matching_items:
            source = matching_items[0]["Source"]
            name = matching_items[0]["Name"]
            embed = discord.Embed(title="MATCH FOUND!", description=name)
            embed.set_image(url=source)
            embed.set_footer(text="Thank You For Using Catto Bot(AniCat)")
            await ctx.send(embed=embed)
            return
        else:

            await ctx.send("Not found")

    except Exception as err:
        await ctx.send("Error occurred: " + str(err))







@anicat.error
async def anicat_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = error.retry_after
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        embed = discord.Embed(title="This Command Is On CoolDown!",
                              description=f"You can use this command again after {str(minutes)} minutes"
                              )
        embed.set_footer(text="Thank You For Using Catto Bot(AniCat)")
        await ctx.send(embed=embed)


@anicatinfo.error
async def anicatinfo_error(ctx, error):
    with open('prefixes.json', 'r') as f: 

        prefixes = json.load(f)
    embed= discord.Embed(title="Error!", description=f"Error While Retrieving Data. Please Try Again Later")
    embed.add_field(inline=False, name="Format", value=f"The Correct Format is {prefixes[str(ctx.guild.id)]}anicatinfo (characterName)")
    await ctx.send(embed=embed)


                            