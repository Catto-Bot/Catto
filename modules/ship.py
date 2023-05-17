import discord
from discord.ext import commands
import random
from PIL import Image
from io import BytesIO

@commands.command(name="ship")
async def ship(ctx, user: discord.Member):
    relationship = random.randint(1, 100)
    relations = ['Friends', 'Best Friends', 'Enemies', 'Romantic partners', 'Strangers', 'Close friends']
    if 0 <= relationship <= 10:
        relstatus = relations[4]
    elif 10 < relationship <= 30:
        relstatus = relations[2]
    elif 30 < relationship <= 60:
        relstatus = relations[0]
    elif 60 < relationship <= 75:
        relstatus = relations[5]
    elif 75 < relationship <= 90:
        relstatus = relations[1]
    else:
        relstatus = relations[3]

    author_avatar = ctx.author.avatar
    user_avatar = user.avatar

    async with ctx.typing():
        async with ctx.bot.session.get(author_avatar) as response1:
            avatar_image1 = Image.open(BytesIO(await response1.read())).resize((128, 128)).convert('RGBA')

        async with ctx.bot.session.get(user_avatar) as response2:
            avatar_image2 = Image.open(BytesIO(await response2.read())).resize((128, 128)).convert('RGBA')

    merged_image = Image.new('RGBA', (256, 128), (0, 0, 0, 0))
    merged_image.paste(avatar_image1, (0, 0), mask=avatar_image1)
    merged_image.paste(avatar_image2, (128, 0), mask=avatar_image2)

    merged_image_bytes = BytesIO()
    merged_image.save(merged_image_bytes, format='PNG')
    merged_image_bytes.seek(0)

    embed = discord.Embed(title="Merged Avatars", description=f"Relationship: {relstatus}")
    embed.set_image(url="attachment://merged_avatars.png")

    await ctx.send(embed=embed, file=discord.File(merged_image_bytes, 'merged_avatars.png'))
