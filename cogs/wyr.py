import contextlib
import re

import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command


class WyrView(discord.ui.View):
    def __init__(self, option1: str, option2: str, *, timeout: float = 30.0):
        super().__init__(timeout=timeout)
        self.option1 = option1
        self.option2 = option2
        self.votes: dict[int, int] = {}  # user_id -> 0 or 1
        self.message: discord.Message | None = None

    def _embed(self) -> discord.Embed:
        c1 = sum(1 for v in self.votes.values() if v == 0)
        c2 = sum(1 for v in self.votes.values() if v == 1)
        embed = discord.Embed(title="WOULD YOU RATHER?", color=0x333333)
        embed.add_field(
            name="Would you rather", value=f"{self.option1}\nVotes: {c1}", inline=True
        )
        embed.add_field(name="Or", value=f"{self.option2}\nVotes: {c2}", inline=True)
        return embed

    async def _vote(self, interaction: discord.Interaction, choice: int) -> None:
        self.votes[interaction.user.id] = choice
        await interaction.response.edit_message(embed=self._embed(), view=self)

    @discord.ui.button(label="◀ Option 1", style=discord.ButtonStyle.primary)
    async def opt1(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._vote(interaction, 0)

    @discord.ui.button(label="Option 2 ▶", style=discord.ButtonStyle.primary)
    async def opt2(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._vote(interaction, 1)

    async def on_timeout(self) -> None:
        if self.message is None:
            return
        for child in self.children:
            child.disabled = True
        embed = self._embed()
        embed.title = "Voting closed"
        with contextlib.suppress(discord.NotFound):
            await self.message.edit(embed=embed, view=self)


class WouldYouRather(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="wyr")
    async def wyr(self, ctx: commands.Context):
        log_command(ctx)
        session = await get_session()
        try:
            async with session.get("https://api.truthordarebot.xyz/api/wyr") as resp:
                data = await resp.json()
            question = data["question"]
        except Exception as err:
            await ctx.send(f"Could not fetch a question: {err}")
            return

        options = re.findall(r"rather\s(.*?)\sor\s(.*?)\?", question, re.IGNORECASE)
        if not options:
            await ctx.send(question)
            return
        option1, option2 = options[0]
        view = WyrView(option1, option2)
        view.message = await ctx.send(embed=view._embed(), view=view)

    @commands.hybrid_command(name="truth")
    async def truth(self, ctx: commands.Context):
        log_command(ctx)
        await self._fetch(ctx, "https://api.truthordarebot.xyz/api/truth")

    @commands.hybrid_command(name="dare")
    async def dare(self, ctx: commands.Context):
        log_command(ctx)
        await self._fetch(ctx, "https://api.truthordarebot.xyz/api/dare")

    async def _fetch(self, ctx: commands.Context, url: str):
        msg = await ctx.send("``Fetching..``")
        session = await get_session()
        try:
            async with session.get(url) as resp:
                data = await resp.json()
            await msg.edit(content=f"```{data['question']}```")
        except Exception as err:
            await msg.delete()
            await ctx.send(f"``{err}``")


async def setup(bot: commands.Bot):
    await bot.add_cog(WouldYouRather(bot))
