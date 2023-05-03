from discord.ext import commands
import discord
import sqlite3


conn = sqlite3.connect('responses.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS responses
                (input_text TEXT PRIMARY KEY, response_text TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS blacklist
                (word TEXT PRIMARY KEY)''')

@commands.command(name="learn",aliases=["l"])
async def learn(ctx, *, input_str:str):
    try:
        input_text, response_text = map(str.strip, input_str.split('|'))
        
        cursor.execute('INSERT OR REPLACE INTO responses (input_text, response_text) VALUES (?, ?)', (input_text.lower(), response_text.lower()))
        conn.commit()
        embed=discord.Embed(title="Thank You For Teaching Me!", description=f'I will respond with "{response_text}" when someone says "{input_text}"', color=discord.Color.dark_gray())
        embed.set_thumbnail(url="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/clans/42744725/3c1e97d35e46102992ab5e5799ea2425dbd83566.png")
        embed.set_footer(text="Thank You For Using Catto Chat Bot!")
        await ctx.send(embed=embed)
    except Exception as err:
        embed2 = discord.Embed(title="Wrong Format!", description='The Correct Format is !learn [input sentence] "|" [output sentence]', color=discord.Color.dark_gray())
        embed2.set_footer(text="Thank You For Using Catto Chat Bot!")
        embed2.set_thumbnail(url="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/clans/42744725/3c1e97d35e46102992ab5e5799ea2425dbd83566.png")
        await ctx.send(embed=embed2)
        await ctx.send(err)

@commands.command(name="c", aliases=["s","talk","chat","t"])
async def c(ctx, *input_text: str):
    input_text = ' '.join(input_text)
    cursor.execute('SELECT response_text FROM responses WHERE input_text = ?', (input_text.lower(),))
    result = cursor.fetchone()
    if result is not None:
        embed = discord.Embed(description=result[0], color=discord.Color.dark_gray())
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error!", description="What Do I Say Here?", color=discord.Color.dark_gray())
        embed.set_footer(text='!learn [input sentence] "|" [output sentence]')
        await ctx.send(embed=embed)




               

        


@learn.error
async def learnerr(ctx,error):
    embed = discord.Embed(title="Wrong Format!", description='The Correct Format is !learn [input sentence] "|" [output sentence]', color=discord.Color.dark_gray())
    embed.set_footer(text="Thank You For Using Catto Chat Bot!")
    embed.set_thumbnail(url="https://cdn.akamai.steamstatic.com/steamcommunity/public/images/clans/42744725/3c1e97d35e46102992ab5e5799ea2425dbd83566.png")
    await ctx.send(embed=embed)


