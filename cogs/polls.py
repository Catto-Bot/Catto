import discord
from discord.ext import commands

from core.logging import log_command

MAX_OPTIONS = 5


class PollButton(discord.ui.Button):
    def __init__(self, idx: int, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.idx = idx

    async def callback(self, interaction: discord.Interaction) -> None:
        view: "PollView" = self.view  # type: ignore[assignment]
        view.votes[interaction.user.id] = self.idx
        await interaction.response.edit_message(embed=view.embed(), view=view)


class PollView(discord.ui.View):
    def __init__(self, question: str, options: list[str], *, timeout: float = 600.0):
        super().__init__(timeout=timeout)
        self.question = question
        self.options = options
        self.votes: dict[int, int] = {}  # user_id -> option index
        for i, label in enumerate(options):
            self.add_item(PollButton(i, label))

    def embed(self) -> discord.Embed:
        counts = [0] * len(self.options)
        for choice in self.votes.values():
            counts[choice] += 1
        total = max(1, sum(counts))
        embed = discord.Embed(title=f"📊 {self.question}", color=discord.Color.gold())
        for i, label in enumerate(self.options):
            pct = counts[i] / total * 100
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            embed.add_field(
                name=label, value=f"`{bar}` {counts[i]} ({pct:.0f}%)", inline=False
            )
        embed.set_footer(text=f"{sum(counts)} vote(s) so far")
        return embed


class Polls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="poll")
    async def poll(self, ctx: commands.Context, *, spec: str):
        """Usage: /poll question | option1 | option2 | option3 ..."""
        log_command(ctx)
        parts = [p.strip() for p in spec.split("|")]
        if len(parts) < 3:
            await ctx.send("Usage: `!poll question | option1 | option2 [...]`")
            return
        question, *options = parts
        if len(options) > MAX_OPTIONS:
            await ctx.send(f"Maximum {MAX_OPTIONS} options.")
            return
        view = PollView(question, options)
        await ctx.send(embed=view.embed(), view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Polls(bot))
