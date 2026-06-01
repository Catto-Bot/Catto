import random
import time

import discord
from discord.ext import commands

from core import db
from core.logging import log_command

DAILY_AMOUNT = 10_000
WEEKLY_AMOUNT = 100_000
DAILY_SECONDS = 86_400
WEEKLY_SECONDS = 604_800
STEAL_COOLDOWN = 25


class Gambler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _ensure_wallet_or_error(self, ctx: commands.Context) -> bool:
        if await db.wallet_exists(ctx.author.id):
            return True
        prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else "!"
        embed = discord.Embed(
            description=f"Use {prefix}monie to create a wallet first", color=0x555555
        )
        await ctx.send(embed=embed)
        return False

    @commands.hybrid_group(name="economy", aliases=["eco"], fallback="balance", description="Catomonie economy commands")
    async def economy(self, ctx: commands.Context, member: discord.Member | None = None):
        """Default: show your balance."""
        await self.balance.callback(self, ctx, member)

    @economy.command(name="monie", description="Create your catomonie wallet")
    async def monie(self, ctx: commands.Context):
        log_command(ctx)
        if await db.wallet_exists(ctx.author.id):
            await ctx.send(embed=discord.Embed(description="You already have a wallet!", color=0x555555))
            return
        await db.create_wallet(ctx.author.id, str(ctx.author))
        prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else "!"
        embed = discord.Embed(
            title="Welcome to Catto Gamble",
            description=f"Start playing with {prefix}bet and claim daily coins with {prefix}daily",
            color=0x555555,
        )
        await ctx.send(embed=embed)

    @economy.command(name="daily", description="Claim your daily catomonie reward")
    async def daily(self, ctx: commands.Context):
        log_command(ctx)
        if not await self._ensure_wallet_or_error(ctx):
            return
        wallet = await db.get_wallet(ctx.author.id)
        now = int(time.time())
        elapsed = now - wallet["last_daily"]
        if elapsed < DAILY_SECONDS:
            hours_left = 24 - round(elapsed / 3600)
            embed = discord.Embed(
                title="Catto Gamble",
                description=f"You can claim once every 24 hours!\n{hours_left} hours left.",
                color=0x333333,
            )
            await ctx.send(embed=embed)
            return
        await db.claim_daily(ctx.author.id, now, DAILY_AMOUNT)
        embed = discord.Embed(
            title=f"{ctx.author}'s Daily Reward",
            description=f"You earned {DAILY_AMOUNT} catomonie!",
            color=0x777777,
        )
        embed.set_footer(text="Thank you for playing catto gamble!")
        await ctx.send(embed=embed)

    @economy.command(name="weekly", description="Claim your weekly catomonie reward")
    async def weekly(self, ctx: commands.Context):
        log_command(ctx)
        if not await self._ensure_wallet_or_error(ctx):
            return
        wallet = await db.get_wallet(ctx.author.id)
        now = int(time.time())
        elapsed = now - wallet["last_weekly"]
        if elapsed < WEEKLY_SECONDS:
            left = WEEKLY_SECONDS - elapsed
            days, rem = divmod(left, 86_400)
            hours = rem // 3600
            embed = discord.Embed(
                title="Catto Gamble",
                description=f"You can claim once a week!\n{days} days, {hours} hours left.",
                color=0x333333,
            )
            await ctx.send(embed=embed)
            return
        await db.claim_weekly(ctx.author.id, now, WEEKLY_AMOUNT)
        embed = discord.Embed(
            title=f"{ctx.author}'s Weekly Reward",
            description=f"You earned {WEEKLY_AMOUNT:,} catomonie!",
            color=0x777777,
        )
        embed.set_footer(text="Thank you for playing catto gamble!")
        await ctx.send(embed=embed)

    @economy.command(name="bal", aliases=["wallet"], description="Show your or someone else's catomonie balance")
    async def balance(self, ctx: commands.Context, member: discord.Member | None = None):
        log_command(ctx)
        target = member or ctx.author
        wallet = await db.get_wallet(target.id)
        if not wallet:
            prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else "!"
            await ctx.send(
                embed=discord.Embed(description=f"Use {prefix}monie to create a wallet first!")
            )
            return
        embed = discord.Embed(
            title=f"{target}'s Balance",
            description=f"Balance: **{wallet['coins']:,}**",
            color=0x555555,
        )
        await ctx.send(embed=embed)

    @economy.command(name="bet", description="Bet catomonie on a number 1-N to win amount * number")
    async def bet(self, ctx: commands.Context, number: int, amount: int):
        log_command(ctx)
        if not await self._ensure_wallet_or_error(ctx):
            return
        if amount < 100 or amount > 25_000:
            await ctx.send(
                embed=discord.Embed(
                    title="Bet amount must be between 100 and 25,000 catomonie!",
                    color=discord.Color.red(),
                )
            )
            return
        if number < 1 or number > 50:
            await ctx.send(
                embed=discord.Embed(
                    title="Number must be between 1 and 50!", color=discord.Color.red()
                )
            )
            return
        max_n = round((amount - 100) * (25 - 5) / (25_000 - 100) + 5)
        if number > max_n:
            await ctx.send(
                embed=discord.Embed(
                    title=f"For that bet amount, the number must be between 1 and {max_n}!",
                    color=discord.Color.red(),
                )
            )
            return
        wallet = await db.get_wallet(ctx.author.id)
        if wallet["coins"] < amount:
            await ctx.send(
                embed=discord.Embed(
                    title="You don't have enough catomonie!", color=discord.Color.red()
                )
            )
            return
        roll = random.randint(1, max_n)
        if number == roll:
            payout = amount * number
            await db.update_coins(ctx.author.id, payout - amount)
            embed = discord.Embed(
                title="Congratulations, you won!",
                description=f"You won {payout:,} catomonie!",
                color=discord.Color.green(),
            )
        else:
            await db.update_coins(ctx.author.id, -amount)
            pct = round(1 / max_n * 100)
            embed = discord.Embed(
                title="Better luck next time!",
                description=f"You had a {pct}% chance.",
                color=discord.Color.red(),
            )
            embed.set_footer(text=f"The number was {roll}")
        await ctx.send(embed=embed)

    @economy.command(name="steal", description="Attempt to steal catomonie from another member (50/50)")
    @commands.cooldown(1, STEAL_COOLDOWN, commands.BucketType.user)
    async def steal(self, ctx: commands.Context, member: discord.Member):
        log_command(ctx)
        if member.id == ctx.author.id:
            await db.update_coins(ctx.author.id, -1000)
            await ctx.send(
                embed=discord.Embed(
                    title="You can't steal from yourself!",
                    description="You lost 1000 catomonie for your idiotness.",
                    color=0xFF7B7B,
                )
            )
            return
        if not await self._ensure_wallet_or_error(ctx):
            return
        target_wallet = await db.get_wallet(member.id)
        if not target_wallet:
            await ctx.send(f"{member.name} hasn't created a wallet yet!")
            return
        my_wallet = await db.get_wallet(ctx.author.id)
        if my_wallet["coins"] < 1000:
            await ctx.send(
                embed=discord.Embed(
                    title="Why So Poor? :C",
                    description="You need at least 1000 to steal.",
                    color=discord.Color.red(),
                )
            )
            return
        if target_wallet["coins"] < 1000:
            await ctx.send(
                embed=discord.Embed(
                    description="They don't have enough money. :C", color=discord.Color.red()
                )
            )
            return
        total = min(my_wallet["coins"], target_wallet["coins"])
        win_money = random.randint(1000, max(1000, int(total / 6)))
        if random.randint(1, 100) <= 50:
            await db.transfer(member.id, ctx.author.id, win_money)
            win_msgs = [
                f"{member.name} fell down the stairs trying to catch you",
                f"You were too quick for {member.name}",
                f"Nice job! {member.name} didn't even notice",
            ]
            await ctx.send(
                embed=discord.Embed(
                    title=f"You won {win_money:,} catomonie", description=random.choice(win_msgs)
                )
            )
        else:
            await db.transfer(ctx.author.id, member.id, win_money)
            lose_msgs = [
                "You fell down the stairs trying to run away",
                f"{member.name} saw through your scheme",
                "You got caught!",
            ]
            await ctx.send(
                embed=discord.Embed(
                    title=f"You lost {win_money:,} catomonie", description=random.choice(lose_msgs)
                )
            )

    @economy.command(name="leaderboard", aliases=["lb"], description="Top 10 catomonie holders")
    async def leaderboard(self, ctx: commands.Context):
        log_command(ctx)
        top = await db.top_wallets(10)
        if not top:
            await ctx.send("No wallets yet!")
            return
        embed = discord.Embed(title="Top 10 Users with Most Money", color=discord.Color.red())
        for i, w in enumerate(top, 1):
            embed.add_field(
                name=f"#{i}: {w['username']}", value=f"Coins: {w['coins']:,}", inline=False
            )
        await ctx.send(embed=embed)

    @economy.command(name="give", description="Send catomonie to another member")
    async def give(self, ctx: commands.Context, amount: int, member: discord.Member):
        log_command(ctx)
        if amount <= 0:
            await ctx.send("Amount must be positive.")
            return
        if not await db.wallet_exists(ctx.author.id):
            await ctx.send("You don't have a wallet!")
            return
        if not await db.wallet_exists(member.id):
            await ctx.send(f"{member.name} doesn't have a wallet!")
            return
        sender = await db.get_wallet(ctx.author.id)
        if sender["coins"] < amount:
            await ctx.send("You don't have enough money!")
            return
        await db.transfer(ctx.author.id, member.id, amount)
        embed = discord.Embed(
            title="Success!",
            description=f"{ctx.author.name} has sent {amount:,} to {member.name}",
        )
        embed.set_footer(text="Thank you for using Catto Bot!")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Gambler(bot))
