from discord.ext import commands
import discord
import sqlite3



@commands.command(name="learn")
async def learn(ctx, input:str, output:str):

    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS responses
                (input_text TEXT PRIMARY KEY, response_text TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS blacklist
                (word TEXT PRIMARY KEY)''')
    cursor.execute('INSERT OR REPLACE INTO responses (input_text, response_text) VALUES (?, ?)', (input.lower(), output.lower()))
    conn.commit()
    embed=discord.Embed(title="Thank You For Teaching Me!", description=f'I will respond with "{input}" when someone says "{output}"', color=discord.Color.dark_gray())
    embed.set_thumbnail(url="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/clans/42744725/3c1e97d35e46102992ab5e5799ea2425dbd83566.png")
    embed.set_footer(text="Thank You For Using Catto Chat Bot!")
    await ctx.send(embed=embed)
    cursor.close()
    conn.close()


@learn.error
async def learnerr(ctx,error):
    embed = discord.Embed(title="Wrong Format!", description="The Coreect Format is !learn [input sentence] [output sentence]", color=discord.Color.dark_gray())
    embed.set_footer(text="Thank You For Using Catto Chat Bot!")
    embed.set_thumbnail(url="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/clans/42744725/3c1e97d35e46102992ab5e5799ea2425dbd83566.png")
    await ctx.send(embed=embed)