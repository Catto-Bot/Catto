import contextlib
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from core import db


class ConfessionModal(discord.ui.Modal, title="Send Confession"):
    confession = discord.ui.TextInput(
        label="Your confession",
        style=discord.TextStyle.paragraph,
        max_length=1900,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        channel_id = await db.get_confession_channel(interaction.guild_id)
        if channel_id is None:
            await interaction.response.send_message(
                "This server has no confession channel set up. Ask an admin to run `/confessionsetup`.",
                ephemeral=True,
            )
            return
        channel = interaction.guild.get_channel(channel_id)
        if channel is None:
            await interaction.response.send_message(
                "Configured confession channel no longer exists.", ephemeral=True
            )
            return
        embed = discord.Embed(
            description=str(self.confession),
            color=discord.Color.green(),
            timestamp=datetime.now(),
        )
        embed.set_footer(text="Anonymous confession")
        await channel.send(embed=embed)
        await interaction.response.send_message("Confession sent anonymously.", ephemeral=True)


class Confession(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="confessionsetup", description="Set the channel where anonymous confessions are posted")
    @commands.has_permissions(administrator=True)
    async def confessionsetup(self, ctx: commands.Context, channel: discord.TextChannel):
        await db.set_confession_channel(ctx.guild.id, channel.id)
        await ctx.send(f"Confession channel set to {channel.mention}")

    @app_commands.command(name="confess", description="Send an anonymous confession")
    async def confess(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(ConfessionModal())

    # Backward-compatible !ch (prefix only) — kept so old users aren't broken
    @commands.command(name="ch")
    async def ch(self, ctx: commands.Context, *, message: str):
        configured = await db.get_confession_channel(ctx.guild.id)
        if configured is None:
            return
        channel = ctx.guild.get_channel(configured)
        if channel is None:
            return
        with contextlib.suppress(discord.Forbidden, discord.NotFound):
            await ctx.message.delete()
        embed = discord.Embed(
            description=message,
            color=discord.Color.green(),
            timestamp=datetime.now(),
        )
        embed.set_footer(text="Anonymous confession")
        await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Confession(bot))
