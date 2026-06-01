import asyncio

import discord
from discord.ext import commands

from core.logging import log_command


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ticketsetup")
    @commands.has_permissions(administrator=True)
    async def ticketsetup(self, ctx: commands.Context):
        log_command(ctx)
        tickets: dict[int, int] = {}
        embed = discord.Embed(
            title="Catto Ticket Counter",
            description="Is this where you want to set up the ticket system?",
        )
        embed.set_footer(text="React to confirm!")
        confirm_msg = await ctx.send(embed=embed)
        await confirm_msg.add_reaction("👍")
        await confirm_msg.add_reaction("👎")

        def confirm_check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == confirm_msg.id
                and str(reaction.emoji) in ["👍", "👎"]
            )

        try:
            reaction, _ = await ctx.bot.wait_for(
                "reaction_add", timeout=20.0, check=confirm_check
            )
        except TimeoutError:
            await ctx.send("You didn't react in time. Please start over.")
            return

        if str(reaction.emoji) != "👍":
            await confirm_msg.delete()
            abort = await ctx.send("Aborting ticket setup.")
            await asyncio.sleep(5)
            await abort.delete()
            return

        category = discord.utils.get(ctx.guild.categories, name="Catickets")
        if category:
            abort = await ctx.send(
                embed=discord.Embed(
                    title="ABORTING!!", description="Category already exists", color=0xFF0000
                )
            )
            await asyncio.sleep(5)
            await abort.delete()
            return

        category = await ctx.guild.create_category("Catickets")
        embed = discord.Embed(title="Welcome to Catickets!", description="React to open a ticket")
        embed.set_thumbnail(
            url="https://img.freepik.com/premium-vector/cute-cat-is-being-ticket-keeper-animal-cartoon-concept-isolated_556653-2544.jpg"
        )
        embed.set_footer(text="Thank you for using Catickets!")
        ticket_msg = await ctx.send(embed=embed)
        await ticket_msg.add_reaction("🎟️")
        await confirm_msg.delete()

        def ticket_check(reaction, user):
            return (
                reaction.message.id == ticket_msg.id
                and str(reaction.emoji) == "🎟️"
                and user != ctx.bot.user
            )

        while True:
            try:
                reaction, user = await ctx.bot.wait_for("reaction_add", check=ticket_check)
            except Exception:
                continue
            if user.id in tickets:
                msg = await ctx.send(f"{user.mention}, you already have a ticket!")
                await msg.delete(delay=5)
                continue
            channel = await ctx.guild.create_text_channel(
                name=f"{user.name}'s ticket", category=category
            )
            await channel.set_permissions(user, read_messages=True, send_messages=True)
            await channel.set_permissions(
                ctx.guild.default_role, read_messages=False, send_messages=False
            )
            embed = discord.Embed(
                title=f"Ticket {user.name} created",
                description=f"{user.mention}, ping a staff member if you need help.",
                color=discord.Color.dark_gray(),
            )
            embed.set_footer(text="Thank you for using Caticket")
            await channel.send(embed=embed)
            tickets[user.id] = channel.id

    @commands.hybrid_command(name="deleteticket")
    @commands.has_permissions(administrator=True)
    async def deleteticket(self, ctx: commands.Context):
        log_command(ctx)
        sure = await ctx.send("Are you sure you want to delete this channel?")
        await sure.add_reaction("👍")
        await sure.add_reaction("👎")

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == sure.id
                and str(reaction.emoji) in ["👍", "👎"]
            )

        try:
            reaction, _ = await ctx.bot.wait_for("reaction_add", timeout=20.0, check=check)
            if str(reaction.emoji) == "👍":
                await ctx.channel.delete()
            else:
                await sure.delete()
        except TimeoutError:
            await sure.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
