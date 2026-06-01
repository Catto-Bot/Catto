import discord
from discord.ext import commands

from core import db
from core.logging import log_command


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="profile")
    async def profile(self, ctx: commands.Context, member: discord.Member | None = None):
        log_command(ctx)
        target = member or ctx.author
        wallet = await db.get_wallet(target.id)
        anicat = await db.get_anicat_user(target.id)
        msg_total = await db.get_message_count(target.id)

        embed = discord.Embed(title=f"{target}'s Profile", color=discord.Color.blurple())
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(
            name="💰 Wallet",
            value=f"{wallet['coins']:,}" if wallet else "no wallet",
            inline=True,
        )
        embed.add_field(
            name="😼 AniCats",
            value=f"{anicat['total_cats']} ({anicat['total_pts']} pts)" if anicat else "0",
            inline=True,
        )
        embed.add_field(name="💬 Messages", value=f"{msg_total:,}", inline=True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="topchat")
    async def topchat(self, ctx: commands.Context):
        log_command(ctx)
        top = await db.top_messages(10)
        if not top:
            await ctx.send("No message stats yet.")
            return
        embed = discord.Embed(title="Top 10 Chatters", color=discord.Color.blue())
        for i, row in enumerate(top, 1):
            embed.add_field(
                name=f"#{i}: {row['username']}",
                value=f"{row['total']:,} messages",
                inline=False,
            )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))
