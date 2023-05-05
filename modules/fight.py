from discord.ext import commands
import discord


@commands.command(name="fight")
async def fight(ctx, *, member: discord.Member = None):
    if not member:
        embed = discord.Embed(
            title="You Can't Fight Yourself!",
            description="!fight (user)"
        )
        embed.set_footer(text="Next Time, Mention A User To Fight :D")
        await ctx.send(embed=embed)
    if member:
        member_health = 100
        author_health = 100
        embed = discord.Embed(
            title=f"{ctx.author.name} VS {member.name}"
        )
        embed.add_field(name=f"{ctx.author.name}'s HP", value=f"{author_health}", inline=True)
        embed.add_field(name=f"{member.name}'s HP", value=f"{member_health}", inline=True)
        embed.add_field(inline=True, name="1", value="Punch",)
        embed.add_field(inline=True, name="2", value="Kick")
        embed.add_field(inline=True, name="3", value="Run")
        embed.set_thumbnail(url="https://w0.peakpx.com/wallpaper/443/933/HD-wallpaper-cat-cartoon-cat-cartoon-black.jpg")
        await ctx.send(embed=embed)