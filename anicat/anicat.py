from discord.ext import commands
import discord
import json
import random

cooldown_time = 6 * 60 * 60
@commands.command(name="anicat")
@commands.cooldown(8, cooldown_time, commands.BucketType.user)
async def anicat(ctx):
    with open("data\data.json", "r", encoding="utf8") as file:
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
        return reaction.message.id == final.id and str(reaction.emoji) in ["<:anicat:1105722682160447550>"]

    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.00, check=check)

        if str(reaction.emoji) == "<:anicat:1105722682160447550>":
            embed = discord.Embed(title=f"claimed by {user}", description="")
            embed.set_image(url=source[random_index])
            embed.set_footer(text=f"Thank You For Using Catto Bot(Anicat)")
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
            else:
                anicatdata[user_name] = {
                    "Total AniCats": 1,
                    "Total AniPoints": points[random_index]
                }

            with open("data/anicat.json", "w") as final:
                json.dump(anicatdata, final)

    except Exception as e:
        editembed = discord.Embed(title="Expired!", description="You Took Too Long To Claim!")
        await final.clear_reactions()
        await final.edit(embed=editembed)



@commands.command(name="anicatinfo")
async def anicatinfo(ctx, *, member: discord.Member = None):
    if member:
        try:
            with open("data/anicat.json", "r", encoding="utf8") as file:
                anicatdata = json.load(file)
            member_name = str(member)
            if member_name in anicatdata:
                total_anicats = anicatdata[member_name]["Total AniCats"]
                total_anipoints = anicatdata[member_name]["Total AniPoints"]

                embed = discord.Embed(title=f"Anicat Info for {member_name}", description="", color=discord.Color.green())
                embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No Record Found")
        except Exception as err:
            await ctx.send("There was a problem!")
    else:
        try:
            with open("data/anicat.json", "r", encoding="utf8") as file:
                anicatdata = json.load(file)
            author_name = str(ctx.author)
            if author_name in anicatdata:
                total_anicats = anicatdata[author_name]["Total AniCats"]
                total_anipoints = anicatdata[author_name]["Total AniPoints"]

                embed = discord.Embed(title=f"Anicat Info for {author_name}", description="", color=discord.Color.magenta())
                embed.add_field(name="Total Anicats", value=total_anicats, inline=False)
                embed.add_field(name="Total AniPoints", value=total_anipoints, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No record found!")
        except Exception as err:
            await ctx.send("There was a problem!")


@anicat.error
async def anicat_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = error.retry_after
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        embed = discord.Embed(title="This Command Is On CoolDown!",
                              description=f"You can use this command again after {hours} and {minutes} minutes"
                              )
        embed.set_footer(text="Thank You For Using Catto Bot(AniCat)")
        await ctx.send(embed=embed)





        
            
    





        
            
    

