import discord
from discord.ext import commands
import random
import requests
from events import events
import json


guessed_word=[]
chosen_word=""
no_of_guesses=0
max_guess=6

@commands.command(name="hangman")
async def hangman(ctx):
    global guessed_word, chosen_word

    string = requests.get("https://random-word-form.herokuapp.com/random/noun").text
    json_string = string
    data = json.loads(json_string)
    chosen_word = data[0]
    print(chosen_word)

    
    
    guessed_word = ['_'] * len(chosen_word)

    embed= discord.Embed(title="Welcome To Hangman \n\nGuess The Word" ,description= " ".join(guessed_word).replace("_", "⬛"),color=0x333333)
    embed.set_footer(text ="Total guesses : 6")
    await ctx.send(embed=embed)



@commands.command(name="guess",aliases=["g"])
async def guess(ctx,guess):
    global chosen_word,guessed_word,no_of_guesses
    if len(guess) !=1:
        await ctx.send("`Enter a single letter`")
        return
    
    if not chosen_word:
        await ctx.send("`Start the game using !hangman`")
        return

    if guess in chosen_word:
        for i in range(len(chosen_word)):
            if chosen_word[i] == guess:
                guessed_word[i] = guess
                    

        if '_' not in guessed_word:
            embed= discord.Embed (title="Correct!", description= " ".join(guessed_word).replace("_", "⬛"),color=0x333333)
            await ctx.send(embed=embed)
            await ctx.send(f"Congratulations, {ctx.message.author.mention} You guessed the correct word `{ ''.join(guessed_word) }`")
            chosen_word=""
            return
    else:
        no_of_guesses +=1

    if no_of_guesses>=max_guess:
        await ctx.send(f"`Game Over, the correct word was {chosen_word}`")
        no_of_guesses=0
        return

    chances_left = max_guess - no_of_guesses  
    embed= discord.Embed (title="Guess The Word", description= " ".join(guessed_word).replace("_", "⬛"),color=0x333333)
    embed.set_footer(text=f"Chances left: {chances_left}")
    await ctx.send(embed=embed)

    

    


    




    




