from discord.ext import commands

cooldown_time = 10


@commands.command(name="emojify", aliases=["e"])
@commands.cooldown(1, cooldown_time, commands.BucketType.user)
async def emojify(ctx, *, msg):
    with open("logs.txt", "a") as file:
        file.write(
            f"\n{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}"
        )
        print(f"{ctx.command.name} command used in '{ctx.guild.name}' Server By {ctx.author}")
    try:
        literalsemojify = {
            "a": "🇦",
            "b": "🇧",
            "c": "🇨",
            "d": "🇩",
            "e": "🇪",
            "f": "🇫",
            "g": "🇬",
            "h": "🇭",
            "i": "🇮",
            "j": "🇯",
            "k": "🇰",
            "l": "🇱",
            "m": "🇲",
            "n": "🇳",
            "o": "🇴",
            "p": "🇵",
            "q": "🇶",
            "r": "🇷",
            "s": "🇸",
            "t": "🇹",
            "u": "🇺",
            "v": "🇻",
            "w": "🇼",
            "x": "🇽",
            "y": "🇾",
            "z": "🇿",
            "0": "0️⃣",
            "1": "1️⃣",
            "2": "2️⃣",
            "3": "3️⃣",
            "4": "4️⃣",
            "5": "5️⃣",
            "6": "6️⃣",
            "7": "7️⃣",
            "8": "8️⃣",
            "9": "9️⃣",
            " ": " ",
        }

        translatedtext = ""
        for char in msg.lower():
            if char in literalsemojify:
                translatedtext += (literalsemojify[char]) + " "

        if translatedtext == "":
            await ctx.send("Your Message Could Not Be Emojified!")
        else:
            await ctx.message.delete()
            await ctx.send(f"{translatedtext}")

    except Exception as err:
        print(err)
        await ctx.send("An unknown error occurred!")


@emojify.error
async def emojify_error(ctx, error):
    await ctx.send("Enter a message as well!")
    print(error)
