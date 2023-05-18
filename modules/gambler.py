from discord.ext import commands
import random
import json
import time
import discord

@commands.command(name="daily")
async def daily(ctx):
    try:
        with open("gamblerdata/catomonie.json", "r") as f:
            catomonie = json.load(f)
    except:
        catomonie = {}
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in catomonie:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        embed = discord.Embed(description=f"Use {prefixes[str(ctx.guild.id)]}monie to create a wallet first", color=0x555555)
        f.close()
        await ctx.send(embed=embed)
    lastClaimed = catomonie[user_id]["last_claimed"]
    currentTime = time.time()
    if currentTime - lastClaimed >= 86400:
        catomonie[user_id]["coins"] += 10000
        catomonie[user_id]["last_claimed"] = currentTime
        with open("gamblerdata/catomonie.json", "w") as final:
            json.dump(catomonie, final)
        embed=discord.Embed(title=f"{user_name}'s Daily Reward", description="You earned 10000 catomonie!", color=0x777777)
        embed.set_footer(text="Thank you for playing catto gamble!")
        await ctx.send(embed=embed)
    else:
        timeleft = currentTime - lastClaimed
        timeleft = 24 - round(timeleft/3600) 
        embed=discord.Embed(title=f"Catto Gamble", description=f"You can claim catomonie once every 24 hours! \n {timeleft} hours until you can claim again!", color=0x333333)
        await ctx.send(embed=embed)


@commands.command(name="weekly")
async def weekly(ctx):
    try:
        with open("gamblerdata/catomonie.json", "r") as f:
            catomonie = json.load(f)
    except:
        catomonie = {}
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in catomonie:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f) 
        embed = discord.Embed(description=f"Use {prefixes[str(ctx.guild.id)]}monie to create a wallet first", color=0x555555)
        await ctx.send(embed=embed)
    last_claimed_weekly = catomonie.get(user_id, {}).get("last_claimed_weekly", 0)
    current_time = time.time()
    if current_time - last_claimed_weekly >= 604800:
        catomonie[user_id] = catomonie.get(user_id, {})
        catomonie[user_id]["coins"] = catomonie[user_id].get("coins", 0) + 100000
        catomonie[user_id]["last_claimed_weekly"] = current_time
        with open("gamblerdata/catomonie.json", "w") as f:
            json.dump(catomonie, f)
        embed = discord.Embed(title=f"{user_name}'s Weekly Reward", description="You earned 100,000 catomonie!", color=0x777777)
        embed.set_footer(text="Thank you for playing catto gamble!")
        await ctx.send(embed=embed)
    else:
        time_left = 604800 - (current_time - last_claimed_weekly)
        days = time_left // 86400
        hours = (time_left - days * 86400) // 3600
        embed = discord.Embed(title=f"Catto Gamble", description=f"You can claim catomonie once a week!\n {int(days)} days and {int(hours)} hours until you can claim again!", color=0x333333)
        await ctx.send(embed=embed)

        

@commands.command(name="monie")
async def monie(ctx):
    try:
        with open("gamblerdata/catomonie.json", "r") as f:
            catomonie = json.load(f)
    except:
        catomonie = {}
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id in catomonie:
        embed = discord.Embed(description="You already have an existing wallet!", color=0x555555)
        await ctx.send(embed=embed)
    else:
        with open('prefixes.json', 'r') as f: 
            prefixes = json.load(f)
    #     
        embed = discord.Embed(title="Welcome to Catto Gamble", description=f"Start playing by using {prefixes[str(ctx.guild.id)]}bet and claim your daily coins with {prefixes[str(ctx.guild.id)]}daily", color=0x555555)
        catomonie[user_id] = {"coins": 0, "last_claimed": 0,"last_claimed_weekly": 0, "Username": user_name}
        f.close()
        with open("gamblerdata/catomonie.json", "w") as final:
            json.dump(catomonie, final)
        await ctx.send(embed=embed)



@commands.command(name="balance" ,aliases=["wallet", "bal"])
async def balance(ctx):
    try:
        with open("gamblerdata/catomonie.json", "r") as f:
            catomonie = json.load(f)
    except:
        catomonie = {}
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    if user_id not in catomonie:
        with open('prefixes.json', 'r') as f: 
            prefixes = json.load(f)    
        embed = discord.Embed(description=f"Use {prefixes[str(ctx.guild.id)]}monie to create a wallet first!")
        await ctx.send(embed=embed)
    else:
        balance = catomonie[user_id]["coins"]
        embed = discord.Embed(title=f"{user_name}'s Balance", description=f"Your balance is **{balance}**.", color=0x555555)
        await ctx.send(embed=embed)


@commands.command(name="bet")
async def bet(ctx,n,m):
    try:
        with open("gamblerdata/catomonie.json", "r") as f:
            catomonie = json.load(f)
    except:
        catomonie = {}
        
    user_id = str(ctx.author.id)
    
    try:
        money = int(m)
        number = int(n)
        
        if user_id not in catomonie:
            embed = discord.Embed(title="Create a wallet first!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        if money < 100 or money > 25000:
            embed = discord.Embed(title="Bet amount should be between 100 and 25,000 catomonie!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if number < 1 or number > 50:
            embed = discord.Embed(title="Number should be between 1 and 50!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        tbd = round((money - 100) * (25 - 5) / (25000 - 100) + 5)
        randomnumber = random.randint(1, int(tbd))
        
        if number > tbd:
            embed = discord.Embed(title=f"For the amount of money that you have given, the number should be between 1 and {tbd}!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        if catomonie[user_id]["coins"] >= money:
            catomonie[user_id]["coins"] -= money
            
            if number == randomnumber:
                total = money * number
                catomonie[user_id]["coins"] += total
                
                embed = discord.Embed(title="Congratulations, you won!", description=f"You won {total} catomonie!", color=discord.Color.green())
                embed.set_footer(text="Thank you for playing catto gamble!")
                await ctx.send(embed=embed)
            else:
                betpercentage = round(1 / tbd * 100)
                
                embed = discord.Embed(title="Better luck next time!", description=f"You had {betpercentage}% chance of winning the bet.", color=discord.Color.red())
                embed.set_footer(text=f"The Number Was {randomnumber}")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="You don't have enough catomonie!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        
        with open("gamblerdata/catomonie.json", "w") as final:
            json.dump(catomonie, final)
    except Exception as err:
        embed = discord.Embed(title="Error!", description="An error occurred while processing your bet. Please try again later.", color=discord.Color.red())
        await ctx.send(embed=embed)

cooldown_time = 25
@commands.command(name="steal")
@commands.cooldown(1, cooldown_time, commands.BucketType.user)
async def steal(ctx, username: discord.Member):
    try:
        try:
            with open("gamblerdata/catomonie.json", "r") as f:
                catomonie = json.load(f)
        except:
            catomonie = {}
        user_id = str(ctx.author.id)
        steal_id = str(username.id)    
        member = username.name
        win_percentage = random.randint(1, 100)

        our_total_money = catomonie[user_id]["coins"]  
        steal_total_money = catomonie[steal_id]["coins"]
        total_money = min(our_total_money,steal_total_money)
        win_money = random.randint(1000,int(round(total_money/3)))
        winmessagearray = [f'{member} fell down the stairs trying to catch you',f'You were too quick for {member}', f'Nice job! {member} didnt even notice you taking their catomonie']
        losemessagearay = [f'You fell down the stairs trying to run away',f'{member} saw through your scheme and gave you a swift kick in your balls', f'You got caught!']
        random_win = random.choice(winmessagearray)
        random_lose = random.choice(losemessagearay)


        if user_id not in catomonie:
            with open('prefixes.json', 'r') as f: 
                prefixes = json.load(f)
            embed = discord.Embed(description=f"Use {prefixes[str(ctx.guild.id)]}monie to create a wallet first!")
            await ctx.send(embed=embed)
            return
        if steal_id not in catomonie:
            embed = discord.Embed(description=f'{member} have not created their wallet yet!')
            await ctx.send(embed=embed)
            return
        if catomonie[user_id]["coins"] < 1000:
            embed = discord.Embed(title="Why So Poor? :C", description="You need atleast 1000 to steal from someone", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        if catomonie[steal_id]["coins"] < 1000:
            embed = discord.Embed(description="They dont have enough money. :C", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if win_percentage <= 50:
            catomonie[steal_id]["coins"] -+ win_money
            catomonie[user_id]["coins"] += win_money
            embed = discord.Embed(title=f'You won {win_money} catomonie', description=random_win)
            await ctx.send(embed=embed)

        else:
            catomonie[steal_id]["coins"] += win_money
            catomonie[user_id]["coins"] -= win_money
            embed = discord.Embed(title=f'You lost {win_money} catomonie', description=random_lose)
            await ctx.send(embed=embed) 

        with open("gamblerdata/catomonie.json", "w") as final:
            json.dump(catomonie, final)   
        

    except discord.ext.commands.errors.MemberNotFound:
        await ctx.send("Invalid member specified.")
    except Exception as err:
        await ctx.send("This person doesn't have a wallet yet!")

@commands.command(name="leaderboard")
async def leaderboard(ctx):
    try:
        with open("gamblerdata/catomonie.json", "r") as f:
            catomonie = json.load(f)
        
        sorted_users = sorted(catomonie.values(), key=lambda x: x['coins'], reverse=True)
        top_10_users = sorted_users[:10]
        embed = discord.Embed(title="Top 10 Users with Most Money", color=discord.Color.red())
        for i, user in enumerate(top_10_users, 1):
            username = user['Username']
            coins = user['coins']
            embed.add_field(name=f"#{i}: {username}", value=f"Coins: {coins}", inline=False)
        await ctx.send(embed=embed)
        
    except Exception as err:
        await ctx.send("Unable To Retrieve Data!")


@steal.error
async def steal_error(ctx, error):
    try:
        with open("gamblerdata/catomonie.json", "r") as f:
            catomonie = json.load(f)
    except:
        catomonie = {} 
    user_id = str(ctx.author.id)
    if catomonie[user_id]["coins"] <= 100:
        embed = discord.Embed(title="Why So Poor? :C", description="Get A Job You Shit", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    catomonie[user_id]["coins"] -= 100
    with open("gamblerdata/catomonie.json", "w") as final:
            json.dump(catomonie, final)
    await ctx.send(error)


@bet.error
async def bet_error(ctx, error):
        with open('prefixes.json', 'r') as f: 
            prefixes = json.load(f)
        embed = discord.Embed(title="Error! Wrong Format", description=f"The Correct format is {prefixes[str(ctx.guild.id)]}bet (number) (money)", color=discord.Color.red())
        await ctx.send(embed=embed)


