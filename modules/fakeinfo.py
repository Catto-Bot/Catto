from discord.ext import commands
import discord
import faker
from faker import Faker

@commands.command(name="fakeinfo")
async def fakeinfo(ctx):
    fake = Faker(['en_NP'])
    for _ in range(10):
        await ctx.send(fake.name())
