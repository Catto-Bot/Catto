import discord
from discord.ext import commands
import requests
import re

def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")

@commands.command(name="wyr")
async def wyr(ctx):
    save(ctx)
    try:
        api_url = "https://would-you-rather-api--abaanshanid.repl.co/"
        response = requests.get(api_url)
        data = response.json()
        question  = data['data']

        # Find the options using regular expressions
        options = re.findall(r"rather\s(.*?)\sor\s(.*?)\?", question, re.IGNORECASE)

        if options:
            option1 = options[0][0]
            option2 = options[0][1]
    
        embed = discord.Embed(title="WHAT WOULD YOU?", color=0x333333)
        embed.add_field(name="Would you rather", value=option1, inline=True)
        embed.add_field(name="Or", value=option2, inline=True)
        message = await ctx.send(embed=embed)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
    

        voted_users = set()  # Set to store the users who have voted
        vote_count = {option1: 0, option2: 0}  # Dictionary to store the vote count

        # Define a check function to filter reactions
        def check(reaction, user):
            return (
                reaction.message.id == message.id
                and user != ctx.bot.user
                and str(reaction.emoji) in ["⬅️", "➡️"]
                and user.id not in voted_users
            )

        while True:
            reaction, user = await ctx.bot.wait_for("reaction_add", check=check, timeout = 30)
            await message.remove_reaction(reaction, user)
            voted_users.add(user.id)  # Add user to the voted_users set
            if str(reaction.emoji) == "⬅️":
                vote_count[option1] += 1
                await ctx.send(f"``{user} voted for Option 1!``")
            elif str(reaction.emoji) == "➡️":
                vote_count[option2] += 1
                await ctx.send(f"``{user} voted for Option 2!``")

            # Update the embed message with the current vote count
            embed.clear_fields()
            embed.add_field(name="Would you rather", value=f"{option1}\nVotes: {vote_count[option1]}", inline=True)
            embed.add_field(name="Or", value=f"{option2}\nVotes: {vote_count[option2]}", inline=True)
            await message.edit(embed=embed)

    except Exception as error:
        embed2 = discord.Embed(title="time limit reached", color=0x333333)
        embed2.add_field(name="Would you rather", value=option1, inline=True)
        embed2.add_field(name="Or", value=option2, inline=True)
        
        await message.clear_reactions()
        await message.edit(embed=embed2)
        