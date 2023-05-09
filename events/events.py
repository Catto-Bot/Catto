from discord.ext import commands
import discord
import json










async def on_ready():
    print("The bot is ready")


async def on_member_join(member):
    try:
        with open('channelgreet.json', 'r') as f:
            channelgreet = json.load(f)

        guild = member.guild
        guild_id = str(guild.id)

        if guild_id in channelgreet:
            channel_id = channelgreet[guild_id]
            channel = guild.get_channel(int(channel_id))
            embed = discord.Embed(
            title=f"Welcome To Our Server {member}!",
            description="Make Sure To Read The Server Rules 🐱",
            color=discord.Color.dark_gray()
)

            embed.set_image(url="https://media.tenor.com/e976NPZxYp8AAAAd/peep-the-cat-rave-cat.gif")
            embed.set_footer(text="Thank You For Using Catto Bot 🐾", icon_url="https://i.pinimg.com/originals/57/39/74/573974c8b4f31d1c4ebda9aed0b46676.gif")
            await channel.send(embed=embed)
                
    except Exception as e:
        print(f"Error: {e}")
    
async def on_member_remove(member):
    try:
        with open('channelgreet.json', 'r') as f:
            channelgreet = json.load(f)

        guild = member.guild
        guild_id = str(guild.id)

        if guild_id in channelgreet:
            channel_id = channelgreet[guild_id]
            channel = guild.get_channel(int(channel_id))
            embed = discord.Embed(title=f"Sorry To See You Leave {member}!", description="Hope You Had A Great Time!", color=discord.Color.dark_gray())
            embed.set_image(url="https://media.tenor.com/uICGiTPlUpgAAAAd/cat-leaving.gif")
            embed.set_footer(text="Thank You For Using Catto Bot 🐾", icon_url="https://i.pinimg.com/originals/57/39/74/573974c8b4f31d1c4ebda9aed0b46676.gif")
            await channel.send(embed=embed)
        
    except Exception as e:
        print(f"Error: {e}")



async def on_guild_join(guild): 
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f) 

    prefixes[str(guild.id)] = '>'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4) 


async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)

def setup(bot):
    bot.add_listener(on_guild_join)
    bot.add_listener(on_guild_remove)
    bot.add_listener(on_ready)
    bot.add_listener(on_member_join)
    bot.add_listener(on_member_remove)
