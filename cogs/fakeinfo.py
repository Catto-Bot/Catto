import asyncio

import discord
from discord.ext import commands
from faker import Faker
from faker.providers import internet

from core.logging import log_command


class FakeInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.fake = Faker()
        self.fake.add_provider(internet)

    @commands.hybrid_command(name="fakeinfo", description="Generate a fake identity (name, address, SSN, etc.)")
    async def fakeinfo(self, ctx: commands.Context):
        log_command(ctx)
        embed = discord.Embed(title="Generating Info, Please Wait! ⏲", description="")
        first = await ctx.reply(embed=embed)
        await asyncio.sleep(1)
        await first.edit(embed=discord.Embed(title="Accessing The Database!", description=""))
        await asyncio.sleep(1)

        fake = self.fake
        info = (
            f"Name: {fake.name()}\n"
            f"Address: {fake.address()}\n"
            f"IP Address: {fake.ipv4_private()}\n"
            f"Job: {fake.job()}\n"
            f"Company: {fake.company()}\n"
            f"Username: {fake.user_name()}\n"
            f"Password: {fake.password()}\n"
            f"Date of Birth: {fake.date_of_birth()}\n"
            f"SSN: {fake.ssn()}\n"
            f"Phone Number: {fake.phone_number()}\n"
            f"Email: {fake.email().split('@')[0]}@gmail.com\n"
            f"Credit Card Number: {fake.credit_card_number()}\n"
            f"Credit Card Provider: {fake.credit_card_provider()}"
        )
        result = discord.Embed(title="Info Generated!", description=info)
        result.set_footer(text="Don't Do Anything Sketchy. We Are Watching You :>")
        await first.edit(embed=result)


async def setup(bot: commands.Bot):
    await bot.add_cog(FakeInfo(bot))
