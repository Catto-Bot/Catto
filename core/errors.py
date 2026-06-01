import logging
import traceback

import discord
from discord import app_commands
from discord.ext import commands

_logger = logging.getLogger("catto")


def _user_facing(error: Exception) -> str:
    if isinstance(error, commands.CommandOnCooldown):
        return f"This command is on cooldown. Try again in {round(error.retry_after)}s."
    if isinstance(error, commands.MissingPermissions):
        return "You don't have permission to use this command."
    if isinstance(error, commands.MissingRequiredArgument):
        return f"Missing argument: `{error.param.name}`."
    if isinstance(error, commands.BadArgument):
        return f"Bad argument: {error}"
    if isinstance(error, commands.CheckFailure):
        return "You can't use this command here."
    if isinstance(error, commands.CommandNotFound):
        return ""  # swallow
    return "Something went wrong. The error has been logged."


def attach(bot: commands.Bot) -> None:
    @bot.event
    async def on_command_error(ctx: commands.Context, error: Exception) -> None:
        original = getattr(error, "original", error)
        msg = _user_facing(error)
        if msg:
            try:
                await ctx.send(embed=discord.Embed(title="Error", description=msg))
            except discord.HTTPException:
                pass
        if not isinstance(
            error,
            (
                commands.CommandOnCooldown,
                commands.MissingPermissions,
                commands.MissingRequiredArgument,
                commands.BadArgument,
                commands.CheckFailure,
                commands.CommandNotFound,
            ),
        ):
            _logger.error(
                "Unhandled error in %s by %s: %s\n%s",
                ctx.command,
                ctx.author,
                original,
                "".join(traceback.format_exception(type(original), original, original.__traceback__)),
            )

    @bot.tree.error
    async def on_app_command_error(
        interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        original = getattr(error, "original", error)
        if isinstance(error, app_commands.CommandOnCooldown):
            msg = f"This command is on cooldown. Try again in {round(error.retry_after)}s."
        elif isinstance(error, app_commands.MissingPermissions):
            msg = "You don't have permission to use this command."
        elif isinstance(error, app_commands.CheckFailure):
            msg = "You can't use this command here."
        else:
            msg = "Something went wrong. The error has been logged."
            _logger.error(
                "Unhandled app command error: %s\n%s",
                original,
                "".join(traceback.format_exception(type(original), original, original.__traceback__)),
            )
        embed = discord.Embed(title="Error", description=msg)
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
