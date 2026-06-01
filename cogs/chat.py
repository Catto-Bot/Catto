import discord
from discord.ext import commands

from core import db
from core.logging import log_command


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="learn", aliases=["l"], description="Teach the bot: <input> | <response>")
    async def learn(self, ctx: commands.Context, *, input_str: str):
        log_command(ctx)
        try:
            input_text, response_text = (s.strip() for s in input_str.split("|", 1))
        except ValueError:
            embed = discord.Embed(
                title="Wrong format!",
                description='Use !learn [input] "|" [response]',
                color=discord.Color.dark_gray(),
            )
            await ctx.send(embed=embed)
            return
        await db.set_chat_response(input_text, response_text)
        embed = discord.Embed(
            title="Thank you for teaching me!",
            description=f'I will respond with "{response_text}" when someone says "{input_text}"',
            color=discord.Color.dark_gray(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="c", aliases=["s", "talk", "chat", "t"], description="Look up a learned response")
    async def c(self, ctx: commands.Context, *, input_text: str):
        log_command(ctx)
        response = await db.get_chat_response(input_text)
        if response:
            await ctx.send(embed=discord.Embed(description=response, color=discord.Color.dark_gray()))
            return
        prefix = await db.get_prefix(ctx.guild.id) if ctx.guild else db.DEFAULT_PREFIX
        embed = discord.Embed(
            title="Error!", description="What do I say here?", color=discord.Color.dark_gray()
        )
        embed.set_footer(text=f"{prefix}learn [input] | [response]")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
