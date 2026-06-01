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
from core.views import ConfirmView

load_dotenv()
HUGGING_FACE_KEY = os.getenv("HUGGING_FACE_KEY")
SD_MODEL_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"


class AIImage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lock = asyncio.Lock()

    @commands.hybrid_command(name="aiterms", description="Read and accept the terms before using the AI image generator")
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
        embed.set_footer(text="Click Yes to agree.")
        view = ConfirmView(ctx.author.id, timeout=30.0)
        msg = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value is True:
            await db.add_ai_allowed(ctx.author.id)
            await msg.edit(content=f"``Access granted to {ctx.author.name}.``", embed=None)
        elif view.value is False:
            await msg.edit(content="``Aborted.``", embed=None)
        else:
            await msg.edit(content="``Expired.``", embed=None)

    @commands.hybrid_command(name="ai", description="Generate an AI image from a text prompt")
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
