from discord.ext import commands
import discord
import json
from easy_pil import Canvas, Font
import io
from discord import File
from easy_pil import Editor, load_image_async, Font
from discord import SyncWebhook

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
            color=discord.Color.dark_gray())

            embed.set_image(url="https://media.tenor.com/e976NPZxYp8AAAAd/peep-the-cat-rave-cat.gif")
            embed.set_thumbnail(url="https://w7.pngwing.com/pngs/885/246/png-transparent-cat-pusheen-desktop-animation-cute-stickers-mammal-animals-cat-like-mammal.png")
            embed.set_footer(text="Thank You For Using Catto Bot 🐾", icon_url="https://i.pinimg.com/originals/57/39/74/573974c8b4f31d1c4ebda9aed0b46676.gif")
            await channel.send(embed=embed)
                
    except Exception as e:
        print(f"Error: {e}")
    


    
    
async def on_member_remove(member):
    try:
        with open('channeleave.json', 'r') as f:
            channelgreet = json.load(f)

        guild = member.guild
        guild_id = str(guild.id)

        if guild_id in channelgreet:
            channel_id = channelgreet[guild_id]
            channel = guild.get_channel(int(channel_id))
            embed = discord.Embed(title=f"Sorry To See You Leave {member}!", description="Hope You Had A Great Time!", color=discord.Color.dark_gray())
            embed.set_thumbnail(url="https://w7.pngwing.com/pngs/885/246/png-transparent-cat-pusheen-desktop-animation-cute-stickers-mammal-animals-cat-like-mammal.gif")
            embed.set_image(url="https://media.tenor.com/uICGiTPlUpgAAAAd/cat-leaving.png")
            embed.set_footer(text="Thank You For Using Catto Bot 🐾", icon_url="https://i.pinimg.com/originals/57/39/74/573974c8b4f31d1c4ebda9aed0b46676.gif")
            await channel.send(embed=embed)
        
    except Exception as e:
        print(f"Error: {e}")




async def on_message(member):
    if member.author.bot:
        return
    content = member.content.lower()
    
    if content == "gn" or content == "goodnight":
        mention = member.author.mention
        await member.channel.send(f"GoodNight {mention}!")
    
    if content == "gm" or content == "goodmorning":
        mention = member.author.mention
        await member.channel.send(f"GoodMorning {mention}!")

    try:
        with open('messages.json', 'r') as f:
            messages = json.load(f)
        with open("gamblerdata/catomonie.json", "r") as fe:
            catomonie = json.load(fe)
    except:
        messages = {}

    member_id = str(member.author.id) 
    user_name = str(member.author)
    def levelupmsg(level):
            level_message = f"Congratulations, {user_name}! You've reached Level {level}! 🎉"
            embed = discord.Embed(title="Level Up", description=level_message, color=discord.Color.green())
            return embed

    if member_id in messages:
        try:
            messages[member_id]['total_messages'] += 1
            if messages[member_id]['total_messages'] == 1:
                await member.channel.send(embed=levelupmsg(1))

            if messages[member_id]['total_messages'] == 50:
                await member.channel.send(embed=levelupmsg(2))

            if messages[member_id]['total_messages'] == 100:
                await member.channel.send(embed=levelupmsg(3))

            if messages[member_id]['total_messages'] == 500:
                await member.channel.send(embed=levelupmsg(4))

            if messages[member_id]['total_messages'] == 1000:
                await member.channel.send(embed=levelupmsg(5))

            if messages[member_id]['total_messages'] == 5000:
                await member.channel.send(embed=levelupmsg(6))

            if messages[member_id]['total_messages'] == 10000:
                await member.channel.send(embed=levelupmsg(7))

            if messages[member_id]['total_messages'] == 20000:
                await member.channel.send(embed=levelupmsg(8))

            if messages[member_id]['total_messages'] == 20000:
                await member.channel.send(embed=levelupmsg(9))

            if messages[member_id]['total_messages'] == 50000:
                await member.channel.send(embed=levelupmsg(10))


            if messages[member_id]['total_messages'] == 40000:
                await member.channel.send(embed=levelupmsg(11))                
        except Exception as err:
            print(err)
            

    else:
        messages[member_id] = {"total_messages": 1, "Username": user_name}

    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)









async def on_guild_join(guild):
    print("Bot joined")
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    

    channel = discord.utils.get(guild.text_channels)
    if channel is not None:
        embed = discord.Embed(title="Thank you for inviting me!", description="I'm here to assist you.", color=discord.Color.green())
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1108380972950491146/7349e4327248b681dcbfc171091aca07.png")  # Replace with your desired cat image URL
        embed.add_field(name="Basic Commands", value="Here are some basic commands you can use:", inline=False)
        embed.add_field(name="!setprefix <new_prefix>", value="Change the bot's command prefix.", inline=False)
        embed.add_field(name="!ai <prompt>", value="Generate AI images.", inline=False)
        embed.add_field(name="!anicat", value="Display waifus.", inline=False)
        embed.add_field(name="!help", value="Display the full list of available commands.", inline=False)
        embed.set_footer(text="Powered by Catto0")  
        await channel.send(embed=embed)
    else:
        print("The specified channel does not exist in the guild.")


    webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1112180785378754620/1MInuU18lMsdxK7gvI_tIK-2T9yVBHU9VxfmMFpRTx3mLLe_uimjWBiDQk9Yjsr-oJiL")
    webhook.send(f"\n\n ------------------ **NEW BOT JOINED** ------------------ \n\n"
             f"**Guild Name**: `{guild.name}` \n"
             f"**Guild ID**: `{guild.id}` \n"
             f"**Member Count**: `{guild.member_count}`")
    




 


async def on_guild_remove(guild):
    print("bot left")
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)
    webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1112180785378754620/1MInuU18lMsdxK7gvI_tIK-2T9yVBHU9VxfmMFpRTx3mLLe_uimjWBiDQk9Yjsr-oJiL")
    webhook.send(f"\n\n ------------------ **BOT LEFT** ------------------ \n\n"
             f"**Guild Name**: `{guild.name}` \n"
             f"**Guild ID**: `{guild.id}` \n"
             f"**Member Count**: `{guild.member_count}`")

def setup(bot):
    bot.add_listener(on_guild_join)
    bot.add_listener(on_guild_remove)
    bot.add_listener(on_member_join)
    bot.add_listener(on_member_remove)
    bot.add_listener(on_message)
    
