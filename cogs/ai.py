import asyncio
import io
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

from core import db
from core.http import get_session
from core.logging import log_command

load_dotenv()
HUGGING_FACE_KEY = os.getenv("HUGGING_FACE_KEY")
SD_MODEL_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"


class AIImage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lock = asyncio.Lock()

    @commands.hybrid_command(name="aiterms")
    async def aiterms(self, ctx: commands.Context):
        log_command(ctx)
        if await db.is_ai_allowed(ctx.author.id):
            await ctx.send(f"``{ctx.author.name}, you already have access.``")
            return
        embed = discord.Embed(title="Terms and Conditions")
        embed.add_field(
            name="Prohibited Content",
            value="The generation of explicit or NSFW images is strictly prohibited. "
            "Users found generating or sharing such content will be permanently banned.",
        )
        embed.add_field(
            name="Command Usage",
            value="Please refrain from spamming the image generation command excessively.",
        )
        embed.add_field(
            name="User Responsibility",
            value="By using the ai command, you acknowledge and agree that you are solely "
            "responsible for the images generated and their usage.",
        )
        embed.set_footer(text="React ✅ to agree, ❌ to abort.")
        verify = await ctx.send(embed=embed)
        await verify.add_reaction("✅")
        await verify.add_reaction("❌")

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == verify.id
                and str(reaction.emoji) in ["✅", "❌"]
            )

        try:
            reaction, _ = await ctx.bot.wait_for("reaction_add", timeout=20.0, check=check)
        except TimeoutError:
            await verify.edit(embed=discord.Embed(title="Expired"))
            await verify.clear_reactions()
            return

        if str(reaction.emoji) == "✅":
            await db.add_ai_allowed(ctx.author.id)
            await verify.edit(content=f"``Access granted to {ctx.author.name}.``", embed=None)
        else:
            await verify.edit(content="``Aborted.``", embed=None)
        await verify.clear_reactions()

    @commands.hybrid_command(name="ai")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ai(self, ctx: commands.Context, *, msg: str):
        log_command(ctx)
        if not await db.is_ai_allowed(ctx.author.id):
            embed = discord.Embed(
                title="Error",
                description=f"Hi {ctx.author.name}, use ``!aiterms`` first to be authorized.",
            )
            embed.set_footer(text="Support Server: https://discord.gg/cvNa9XTbD9")
            await ctx.send(embed=embed)
            return

        if self.lock.locked():
            await ctx.reply(
                f"Hi {ctx.author.name}, the command is in use. Please wait."
            )
            return

        async with self.lock:
            ret = await ctx.send("Generating image...")
            session = await get_session()
            try:
                async with session.post(
                    SD_MODEL_URL,
                    headers={"Authorization": HUGGING_FACE_KEY},
                    json={"inputs": msg},
                ) as resp:
                    image_bytes = await resp.read()
                image = Image.open(io.BytesIO(image_bytes))
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                buf.seek(0)
                embed = discord.Embed(
                    title="Generated Image", description=f"Prompt: {msg}", color=0x000000
                )
                embed.set_image(url="attachment://output.png")
                embed.set_footer(text="Note: Generating explicit images will result in a ban")
                await ret.delete()
                await ctx.reply(embed=embed, file=discord.File(buf, filename="output.png"))
            except Exception as err:
                await ret.edit(content=f"Image generation failed: {err}")

    @ai.error
    async def ai_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Try again in {round(error.retry_after)} second(s)."
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("``Please enter a prompt!``")


async def setup(bot: commands.Bot):
    await bot.add_cog(AIImage(bot))
