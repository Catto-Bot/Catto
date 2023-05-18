from discord.ext import commands
import discord

#user.avatar_url

@commands.command(name='avatar', aliases=["av"])
async def avatar(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
        userAvatar = member.avatar
        embed= discord.Embed(
            title=f"{member.name}'s Avatar"
        )
        embed.set_image(url=userAvatar)
        await ctx.send(embed=embed)
        return
    if member:
        userAvatar = member.avatar
        embed= discord.Embed(
            title=f"{member.name}'s Avatar"
        )
        embed.set_image(url=userAvatar)
        await ctx.send(embed=embed)
        return

@avatar.error
async def avatar_error(ctx,member):
    embed = discord.Embed(
        title="Error!",
        description="There has been an error while processing the command!!"
    )
    await ctx.send(embed=embed)
   

    

        
