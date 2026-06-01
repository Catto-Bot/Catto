import contextlib

import discord
from discord.ext import commands

from core.logging import log_command

TICKET_CATEGORY = "Catickets"


class OpenTicketButton(discord.ui.View):
    """Persistent view: clicking the button opens a private ticket channel."""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Open Ticket",
        emoji="🎟️",
        style=discord.ButtonStyle.primary,
        custom_id="catto:ticket:open",
    )
    async def open(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("Use this in a server.", ephemeral=True)
            return
        category = discord.utils.get(guild.categories, name=TICKET_CATEGORY)
        if category is None:
            await interaction.response.send_message(
                "Ticket category missing. Run `/ticketsetup` again.", ephemeral=True
            )
            return
        existing = discord.utils.get(category.channels, name=f"ticket-{interaction.user.name.lower()}")
        if existing is not None:
            await interaction.response.send_message(
                f"You already have a ticket: {existing.mention}", ephemeral=True
            )
            return
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True
            ),
        }
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name.lower()}",
            category=category,
            overwrites=overwrites,
        )
        embed = discord.Embed(
            title=f"Ticket for {interaction.user.name}",
            description=f"{interaction.user.mention}, ping a staff member if you need help.",
            color=discord.Color.dark_gray(),
        )
        embed.set_footer(text="Thank you for using Catickets")
        await channel.send(embed=embed)
        await interaction.response.send_message(
            f"Ticket created: {channel.mention}", ephemeral=True
        )


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.add_view(OpenTicketButton())  # restore persistence on cog load

    @commands.hybrid_command(name="ticketsetup", description="Post a persistent ticket-open button in this channel")
    @commands.has_permissions(administrator=True)
    async def ticketsetup(self, ctx: commands.Context) -> None:
        log_command(ctx)
        category = discord.utils.get(ctx.guild.categories, name=TICKET_CATEGORY)
        if category is None:
            category = await ctx.guild.create_category(TICKET_CATEGORY)
        embed = discord.Embed(
            title="Welcome to Catickets!",
            description="Click the button below to open a ticket.",
        )
        embed.set_footer(text="Thank you for using Catickets!")
        await ctx.send(embed=embed, view=OpenTicketButton())

    @commands.hybrid_command(name="deleteticket", description="Delete the current ticket channel")
    @commands.has_permissions(administrator=True)
    async def deleteticket(self, ctx: commands.Context) -> None:
        log_command(ctx)
        from core.views import ConfirmView

        view = ConfirmView(ctx.author.id)
        msg = await ctx.send("Delete this channel?", view=view)
        await view.wait()
        if view.value is True:
            with contextlib.suppress(discord.NotFound):
                await ctx.channel.delete()
        else:
            await msg.edit(content="Cancelled.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
