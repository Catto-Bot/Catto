import discord
from discord.ext import commands

from core.logging import log_command


class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="avatar", aliases=["av"], description="Show a member's avatar in full size")
    async def avatar(self, ctx: commands.Context, member: discord.Member | None = None):
        log_command(ctx)
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Avatar")
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Avatar(bot))
