import discord
from discord.ext import commands 

@commands.command(name="setuprole")
@commands.has_permissions(manage_roles=True)
async def setuprole(ctx, rolename, member: discord.Member = None ):
    if member is None:
        member = ctx.author

    role = discord.utils.get(ctx.guild.roles, name = rolename)
    if role is None:
        await ctx.send(f"Role {rolename} not found!")
    elif role in member.roles:
        await ctx.send(f"{member.mention} already has the {rolename} role!")
    else:
        await member.add_roles(role)
        if member is None:
            await ctx.send(f'Role {rolename} added for {ctx.author.mention}!') 
        else:
            await ctx.send(f'Role {rolename} added for {member.mention}!') 


@commands.command(name="createrole")
@commands.has_permissions(administrator = True)

async def createrole(ctx,rolename):
    guild = ctx.guild
    exisitng_role = discord.utils.get(guild.roles, name = rolename)
    if exisitng_role is None:
        await guild.create_role(name = rolename)
        await ctx.send(f"Role {rolename} has been created!")
    else:
        await ctx.send(f"Role {rolename} already exists!")

@commands.command(name = "deleterole")
@commands.has_permissions(administrator = True)

async def deleterole(ctx, rolename):
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    if role is None:
        await ctx.send(f'Role {rolename} not found!')
    else:
        await role.delete()
        await ctx.send(f'Role {rolename} deleted!')

@commands.command(name = "removerole")
@commands.has_permissions(manage_roles=True)

async def removerole(ctx, rolename, member: discord.Member = None):
    if member is None:
        member = ctx.author
    role = discord.utils.get(ctx.guild.roles, name = rolename)
    if role is None:
        await ctx.send(f"Role {rolename} not found!")
    if not(role in member.roles):
        await ctx.send(f"{member.display_name} does not have the Role {rolename}!")
    else:
        await member.remove_roles(role)
        await ctx.send(f"Removed Role {rolename} from {member.display_name}!")