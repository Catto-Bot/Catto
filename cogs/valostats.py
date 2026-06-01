import random

import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command

JETT = "<:jett:1106205144233816164>"
RAZE = "<:raze:1106205146989465660>"
VANDAL = "<:vandal:1106219261086670859>"
SMOKE = "<:smoke:1106219255252385923>"
SATCHEL = "<:satchel:1106219252555456602>"


class Valostats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="vstats", description="Show Valorant account stats. Usage: username#tag")
    async def vstats(self, ctx: commands.Context, *, name: str):
        log_command(ctx)
        if "#" not in name:
            await ctx.send("Use format: `username#tagline`")
            return
        username, tag = name.split("#", 1)
        loading = await ctx.send("``Retrieving data, please wait``")
        session = await get_session()
        try:
            async with session.get(
                f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}"
            ) as r:
                account = (await r.json())["data"]
            async with session.get(
                f"https://api.henrikdev.xyz/valorant/v1/mmr/ap/{username}/{tag}"
            ) as r:
                rank = (await r.json())["data"]
        except Exception:
            await loading.edit(content="User not found.")
            return
        embed = discord.Embed(
            title=f"{account['name']} #{account['tag']}",
            description=f"Account level: {account['account_level']}",
        )
        embed.set_image(url=account["card"]["wide"])
        embed.set_thumbnail(url=rank["images"]["small"])
        embed.set_footer(text=f"Last Updated: {account['last_update']}")
        await loading.delete()
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="valofight", aliases=["vf"], description="Turn-based Valorant duel against another member")
    async def valofight(self, ctx: commands.Context, member: discord.Member):
        log_command(ctx)
        hp = {ctx.author.id: 150, member.id: 150}
        turn_msg = await ctx.send(
            embed=discord.Embed(
                title=f"{ctx.author.name} (Jett) vs {member.name} (Raze)",
                description=f"{ctx.author.name}'s turn. Vandal or Smoke?",
            )
        )
        await turn_msg.add_reaction(VANDAL)
        await turn_msg.add_reaction(SMOKE)

        while hp[ctx.author.id] > 0 and hp[member.id] > 0:
            # author turn
            def author_check(reaction, user, *, mid=turn_msg.id):
                return (
                    user == ctx.author
                    and reaction.message.id == mid
                    and str(reaction.emoji) in [VANDAL, SMOKE]
                )

            try:
                reaction, _ = await ctx.bot.wait_for(
                    "reaction_add", timeout=20.0, check=author_check
                )
            except TimeoutError:
                await ctx.send("Time limit reached.")
                return
            if str(reaction.emoji) == VANDAL:
                hp[member.id] -= random.randrange(0, 150)
                if hp[member.id] <= 0:
                    await ctx.send(
                        embed=discord.Embed(
                            title=f"{ctx.author.name} (Jett) won the match!",
                            description=f"{ctx.author.name}: {max(hp[ctx.author.id], 0)} HP | {member.name}: 0 HP",
                        )
                    )
                    return
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title=f"{member.name} won by default!",
                        description=f"{ctx.author.name} used Smoke to run away.",
                    )
                )
                return

            # member turn
            turn_msg = await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.name} vs {member.name}",
                    description=(
                        f"{member.name}'s turn. Vandal or Satchel?\n"
                        f"{ctx.author.name}: {hp[ctx.author.id]} HP | "
                        f"{member.name}: {hp[member.id]} HP"
                    ),
                )
            )
            await turn_msg.add_reaction(VANDAL)
            await turn_msg.add_reaction(SATCHEL)

            def member_check(reaction, user, *, mid=turn_msg.id):
                return (
                    user == member
                    and reaction.message.id == mid
                    and str(reaction.emoji) in [VANDAL, SATCHEL]
                )

            try:
                reaction, _ = await ctx.bot.wait_for(
                    "reaction_add", timeout=20.0, check=member_check
                )
            except TimeoutError:
                await ctx.send("Time limit reached.")
                return
            if str(reaction.emoji) == VANDAL:
                hp[ctx.author.id] -= random.randrange(0, 150)
                if hp[ctx.author.id] <= 0:
                    await ctx.send(
                        embed=discord.Embed(
                            title=f"{member.name} (Raze) won the match!",
                            description=f"{ctx.author.name}: 0 HP | {member.name}: {max(hp[member.id], 0)} HP",
                        )
                    )
                    return
            else:
                await ctx.send(
                    embed=discord.Embed(
                        title=f"{ctx.author.name} won by default!",
                        description=f"{member.name} used Satchel to run away.",
                    )
                )
                return

            # next author turn embed
            turn_msg = await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.name} vs {member.name}",
                    description=(
                        f"{ctx.author.name}'s turn. Vandal or Smoke?\n"
                        f"{ctx.author.name}: {hp[ctx.author.id]} HP | "
                        f"{member.name}: {hp[member.id]} HP"
                    ),
                )
            )
            await turn_msg.add_reaction(VANDAL)
            await turn_msg.add_reaction(SMOKE)


async def setup(bot: commands.Bot):
    await bot.add_cog(Valostats(bot))
