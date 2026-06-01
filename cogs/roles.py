import discord
from discord.ext import commands

from core.logging import log_command


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="setuprole", description="Give a role to a member by name")
    @commands.has_permissions(manage_roles=True)
    async def setuprole(
        self, ctx: commands.Context, rolename: str, member: discord.Member | None = None
    ):
        log_command(ctx)
        member = member or ctx.author
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role is None:
            await ctx.send(f"Role {rolename} not found!")
            return
        if role in member.roles:
            await ctx.send(f"{member.mention} already has the {rolename} role!")
            return
        await member.add_roles(role)
        await ctx.send(f"Role {rolename} added for {member.mention}!")

    @commands.hybrid_command(name="createrole", description="Create a new role on this server")
    @commands.has_permissions(administrator=True)
    async def createrole(self, ctx: commands.Context, rolename: str):
        log_command(ctx)
        if discord.utils.get(ctx.guild.roles, name=rolename):
            await ctx.send(f"Role {rolename} already exists!")
            return
        await ctx.guild.create_role(name=rolename)
        await ctx.send(f"Role {rolename} has been created!")

    @commands.hybrid_command(name="deleterole", description="Delete a role from this server")
    @commands.has_permissions(administrator=True)
    async def deleterole(self, ctx: commands.Context, rolename: str):
        log_command(ctx)
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role is None:
            await ctx.send(f"Role {rolename} not found!")
            return
        await role.delete()
        await ctx.send(f"Role {rolename} deleted!")

    @commands.hybrid_command(name="removerole", description="Remove a role from a member by name")
    @commands.has_permissions(manage_roles=True)
    async def removerole(
        self, ctx: commands.Context, rolename: str, member: discord.Member | None = None
    ):
        log_command(ctx)
        member = member or ctx.author
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role is None:
            await ctx.send(f"Role {rolename} not found!")
            return
        if role not in member.roles:
            await ctx.send(f"{member.display_name} does not have the role {rolename}!")
            return
        await member.remove_roles(role)
        await ctx.send(f"Removed role {rolename} from {member.display_name}!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
