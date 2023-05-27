import discord
from discord.ext import commands
import random
import requests
import json

hangman_games = {}

@commands.command(name="hangman")
async def hangman(ctx):
    global hangman_games

    if ctx.guild.id in hangman_games:
        await ctx.send("A Hangman game is already in progress in this server.")
        return
    hello = await ctx.send("``Starting Game, Please Wait``")
    string = requests.get("https://random-word-form.herokuapp.com/random/noun").text
    json_string = string
    data = json.loads(json_string)
    chosen_word = data[0]
    print(chosen_word)

    guessed_word = ['_'] * len(chosen_word)
    no_of_guesses = 0
    max_guess = 6

    hangman_games[ctx.guild.id] = {
        'chosen_word': chosen_word,
        'guessed_word': guessed_word,
        'no_of_guesses': no_of_guesses,
        'max_guess': max_guess
    }
    embed = discord.Embed(title="Welcome To Hangman", description="Use !guess <letter>\n\nGuess The Word: " + " ".join(guessed_word).replace("_", "⬛"), color=0x333333)
    embed.set_footer(text="Total guesses: 6")
    await hello.delete()
    await ctx.send(embed=embed)


@commands.command(name="guess", aliases=["g"])
async def guess(ctx, guess):
    global hangman_games

    if ctx.guild.id not in hangman_games:
        await ctx.send("No Hangman game in progress in this server. Start the game using !hangman.")
        return

    game = hangman_games[ctx.guild.id]
    chosen_word = game['chosen_word']
    guessed_word = game['guessed_word']
    no_of_guesses = game['no_of_guesses']
    max_guess = game['max_guess']

    if len(guess) != 1:
        await ctx.send("Enter a single letter.")
        return

    if guess in chosen_word:
        for i in range(len(chosen_word)):
            if chosen_word[i] == guess:
                guessed_word[i] = guess

        if '_' not in guessed_word:
            embed = discord.Embed(title="Correct!", description=" ".join(guessed_word).replace("_", "⬛"), color=0x333333)
            await ctx.send(embed=embed)
            await ctx.send(f"Congratulations, {ctx.message.author.mention}! You guessed the correct word: {''.join(guessed_word)}")
            del hangman_games[ctx.guild.id]
            return
    else:
        no_of_guesses += 1
        hangman_games[ctx.guild.id]['no_of_guesses'] = no_of_guesses

    if no_of_guesses >= max_guess:
        await ctx.send(f"Game Over! The correct word was {chosen_word}")
        del hangman_games[ctx.guild.id]
        return

    chances_left = max_guess - no_of_guesses
    embed = discord.Embed(title="Guess The Word", description=" ".join(guessed_word).replace("_", "⬛"), color=0x333333)
    embed.set_footer(text=f"Chances left: {chances_left}")
    await ctx.send(embed=embed)



@guess.error
async def guess_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`Correct format is !guess <letter>`")
    