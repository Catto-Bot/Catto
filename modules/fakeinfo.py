from discord.ext import commands
import discord
import faker
from faker import Faker
from faker.providers import internet
import asyncio

@commands.command(name="fakeinfo")
async def fakeinfo(ctx):
    fake = Faker()
    fake.add_provider(internet)
    embed = discord.Embed(title="Generating Info, Please Wait!", description="")
    first = await ctx.send(embed=embed)
    await asyncio.sleep(1)
    embed2 = discord.Embed(title="Accessing The Database!", description="")
    await first.edit(embed=embed2)
    await asyncio.sleep(1)
    third = discord.Embed(title="Almost Done!", description="")
    await first.edit(embed=third)
    
    name = fake.name()
    address = fake.address()
    ip_address = fake.ipv4_private()
    job = fake.job()
    company = fake.company()
    user_name = fake.user_name()
    password = fake.password()
    date_of_birth = fake.date_of_birth()
    ssn = fake.ssn()
    phone_number = fake.phone_number()
    emailoriginal = fake.email().split('@')[0]
    email = emailoriginal + "@gmail.com"
    credit_card_number = fake.credit_card_number()
    credit_card_provider = fake.credit_card_provider()

    info_message = f"Name: {name}\nAddress: {address}\nIP Address: {ip_address}\nJob: {job}\nCompany: {company}\nUsername: {user_name}\nPassword: {password}\nDate of Birth: {date_of_birth}\nSSN: {ssn}\nPhone Number: {phone_number}\nEmail: {email}\nCredit Card Number: {credit_card_number}\nCredit Card Provider: {credit_card_provider}"

    
    fourth = discord.Embed(title="Info Generated!", description=info_message)
    fourth.set_footer(text="Don't Do Anything Sketchy.\nWe Are Watching You :>")
    await first.edit(embed=fourth)

  
    


