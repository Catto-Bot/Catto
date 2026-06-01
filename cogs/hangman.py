import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command


class Hangman(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.games: dict[int, dict] = {}

    @commands.hybrid_command(name="hangman", description="Start a new hangman game in this server")
    async def hangman(self, ctx: commands.Context):
        log_command(ctx)
        if ctx.guild.id in self.games:
            await ctx.send("A Hangman game is already in progress in this server.")
            return
        loading = await ctx.send("``Starting game, please wait``")
        session = await get_session()
        async with session.get("https://random-word-form.herokuapp.com/random/noun") as resp:
            data = await resp.json()
        word = data[0]
        self.games[ctx.guild.id] = {
            "word": word,
            "guessed": ["_"] * len(word),
            "wrong": 0,
            "max": 6,
        }
        embed = discord.Embed(
            title="Welcome To Hangman",
            description="Use !guess <letter>\n\nGuess The Word: "
            + " ".join(["⬛"] * len(word)),
            color=0x333333,
        )
        embed.set_footer(text="Total guesses: 6")
        await loading.delete()
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="guess", aliases=["g"], description="Guess a letter in the current hangman game")
    async def guess(self, ctx: commands.Context, letter: str):
        log_command(ctx)
        game = self.games.get(ctx.guild.id)
        if not game:
            await ctx.send("No Hangman game in progress. Start one with !hangman.")
            return
        if len(letter) != 1:
            await ctx.send("Enter a single letter.")
            return
        if letter in game["word"]:
            for i, c in enumerate(game["word"]):
                if c == letter:
                    game["guessed"][i] = letter
            if "_" not in game["guessed"]:
                embed = discord.Embed(
                    title="Correct!",
                    description=" ".join(game["guessed"]),
                    color=0x333333,
                )
                await ctx.send(embed=embed)
                await ctx.send(
                    f"Congratulations, {ctx.author.mention}! You guessed the word: "
                    f"{''.join(game['guessed'])}"
                )
                del self.games[ctx.guild.id]
                return
        else:
            game["wrong"] += 1

        if game["wrong"] >= game["max"]:
            await ctx.send(f"Game Over! The correct word was {game['word']}")
            del self.games[ctx.guild.id]
            return

        embed = discord.Embed(
            title="Guess The Word",
            description=" ".join(c if c != "_" else "⬛" for c in game["guessed"]),
            color=0x333333,
        )
        embed.set_footer(text=f"Chances left: {game['max'] - game['wrong']}")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Hangman(bot))
