from discord.ext import commands
import discord
import asyncio


def save(ctx):
    with open("logs.txt", "a") as file:
        file.write(f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")

@commands.command(name="ticketsetup")
@commands.has_permissions(administrator=True)
async def ticketsetup(ctx):
    save(ctx)
    tickets = {}
    embed = discord.Embed(title="Catto Ticket Counter", description="Is this where you want to setup the ticket system?")
    embed.set_footer(text="React to confirm!")
    ticketmessage = await ctx.send(embed=embed)
    await ticketmessage.add_reaction("👍")
    await ticketmessage.add_reaction("👎")

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == ticketmessage.id and str(reaction.emoji) in ["👍", "👎"]

    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=check)

        if str(reaction.emoji) == "👍":
            category = discord.utils.get(ctx.guild.categories, name="Catickets")

            if category:
                embed = discord.Embed(title='ABORTING!!',description="Category Already Exists", color=0xff0000)
                abort = await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await abort.delete()
                await ctx.message.delete()
                return
            else:
                category = await ctx.guild.create_category("Catickets")
                loading = await ctx.send("🟢 Loading, Please Wait 🟢")
                embed = discord.Embed(title="Welcome to Catickets!", description="React to get started!")
                embed.set_thumbnail(url="https://img.freepik.com/premium-vector/cute-cat-is-being-ticket-keeper-animal-cartoon-concept-isolated_556653-2544.jpg")
                embed.set_footer(text="Thank you for using Catickets!")
                ticket = await ctx.send(embed=embed)
                await ticket.add_reaction("🎟️")
                await loading.delete()
                await ticketmessage.delete()
                await ctx.message.delete()

                def check(reaction, user):
                    return reaction.message.id == ticket.id and str(reaction.emoji) == "🎟️" and user != ctx.bot.user




                while True:
                    try:
                        reaction, user = await ctx.bot.wait_for('reaction_add', check=check)
                        if str(reaction.emoji) == "🎟️":
                            if user.id in tickets:
                                hello = await ctx.send(f"{user.mention}, You already have a ticket!")
                                await hello.delete(delay=5)
                            else:
                                text_channel = await ctx.guild.create_text_channel(
                                    name=f"{user.name}'s ticket",
                                    category=category
                                )
                                channel = ctx.bot.get_channel(text_channel.id)
                                usermention = await channel.send(user.mention)
                                await usermention.delete()
                                embed= discord.Embed(title=f"Ticket With The Name {user.name} Has Been Created ", description=f"{user.mention}, Ping A Staff Or An Admin If You Need Help.", color=discord.Color.dark_gray())
                                embed.set_footer(text="Thank You For Using Caticket")
                                await channel.send(embed=embed)
                                await text_channel.set_permissions(
                                    user, 
                                    read_messages=True, 
                                    send_messages=True
                                )
                                await text_channel.set_permissions(
                                    ctx.guild.default_role, 
                                    read_messages=False, 
                                    send_messages=False
                                )

                                tickets[user.id] = text_channel.id
                        else:
                            await ctx.send("Invalid reaction. Please start over.")
                    except Exception as err:
                        await ctx.send(f"An Error Occured {err}")

        else:
            await ctx.message.delete()
            await ticketmessage.delete()
            abort = await ctx.send("Aborting ticket setup.")
            await asyncio.sleep(5)
            await abort.delete()
            

    except asyncio.TimeoutError:
        await ctx.send("You didn't react in time. Please start over.")

@commands.command(name="deleteticket")
@commands.has_permissions(administrator=True)
async def deleteticket(ctx):
    save(ctx)
    sure = await ctx.send("Are you sure you want to delete this channel?")
    await sure.add_reaction("👍")
    await sure.add_reaction("👎")
    def check(reaction, user):
        return user == ctx.author and reaction.message.id == sure.id and str(reaction.emoji) in ["👍", "👎"]
    
    try:
        reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20.0, check=check)
        if str(reaction.emoji) == "👍":
            await ctx.send("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            await ctx.channel.delete()
        else:
            await sure.delete()
    except Exception as err:
        await ctx.send("An error ocurred while deleting the channel")

@ticketsetup.error
async def ticketsetup_error(ctx, error):
    embed = discord.Embed(title="You don't have permission to run this command!", color=0xff0000)
    await ctx.send(embed=embed)


                
            


