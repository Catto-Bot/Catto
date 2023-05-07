from discord.ext import commands
import discord
import json
import requests


@commands.command(name="hug")
async def hug(ctx, member: commands.MemberConverter = None):
    if member:
        hugr = requests.get("https://purrbot.site/api/img/sfw/hug/gif")
        json_hug_data = json.loads(hugr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} hugs {member.display_name}! AWWWWW ❁◕ ‿ ◕❁", color=discord.Color.dark_gray())
        embed.set_image(url=json_hug_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Hugged Yourself! ❁◕ ‿ ◕❁")
         embed.set_footer(text="Next Time Mention A User To Hug :D")
         embed.set_image(url="https://media.tenor.com/XEEmDlNSmEcAAAAM/spongebob-love.gif")
         await ctx.send(embed=embed)

@commands.command(name="slap")
async def slap(ctx, member: commands.MemberConverter = None):
    if member:
        hugr = requests.get("https://purrbot.site/api/img/sfw/slap/gif")
        json_hug_data = json.loads(hugr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} slaps {member.display_name}! OUCH ( ಥ۝ಥ )", color=discord.Color.dark_gray())
        embed.set_image(url=json_hug_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You slapped Yourself! ( ಥ۝ಥ )")
         embed.set_footer(text="Next Time Mention A User To Slap :D")
         embed.set_image(url="https://media.tenor.com/rXAnv88yrFwAAAAM/anime-slapping-face.gif")
         await ctx.send(embed=embed)

@commands.command(name="kiss")
async def kiss(ctx, member: commands.MemberConverter = None):
    if member:
        hugr = requests.get("https://purrbot.site/api/img/sfw/kiss/gif")
        json_hug_data = json.loads(hugr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} kisses {member.display_name}! AWWWW (ᅌwᅌ)", color=discord.Color.dark_gray())
        embed.set_image(url=json_hug_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Can't Kiss Yourself! ( ಥ۝ಥ )")
         embed.set_footer(text="Next Time Mention A User To Kiss :D")
         await ctx.send(embed=embed)

@commands.command(name="bite")
async def bite(ctx, member: commands.MemberConverter = None):
    if member:
        biter = requests.get("https://purrbot.site/api/img/sfw/bite/gif")
        json_bite_data = json.loads(biter.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} bites {member.display_name}! OUCH! (ಥ۝ಥ)", color=discord.Color.dark_gray())
        embed.set_image(url=json_bite_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Bit Yourself! ( ಥ۝ಥ )")
         embed.set_image(url="https://media.tenor.com/D7XNyUe6Q7UAAAAS/hit-self-kitten.gif")
         embed.set_footer(text="Next Time Mention A User To Kiss :D")
         await ctx.send(embed=embed)

@commands.command(name="lick")
async def lick(ctx, member: commands.MemberConverter = None):
    if member:
        lickr = requests.get("https://purrbot.site/api/img/sfw/lick/gif")
        json_lick_data = json.loads(lickr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} Licks {member.display_name}! AWWWWW! (✿ ♥‿♥)(♥ω♥*)", color=discord.Color.dark_gray())
        embed.set_image(url=json_lick_data['link'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title="You Licked Yourself! ♥‿♥")
         embed.set_image(url="https://media.tenor.com/6StCIWYFkOcAAAAC/adalfarus-adal.gif")
         embed.set_footer(text="Next Time Mention A User To Lick :D")
         await ctx.send(embed=embed)


#         category = ["waifu",
#
# "wave",
# "handhold",
# "nom",
# "kill",
# "kick",
# "wink",
# "poke",
# "dance",
# "cringe"]
@commands.command(name="bully")
async def bully(ctx, member: commands.MemberConverter = None):
    if member:
        bullyr = requests.get("https://api.waifu.pics/sfw/bully")
        json_bully_data = json.loads(bullyr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} Bullied {member.display_name}!! (ಥ﹃ಥ)", color=discord.Color.dark_gray())
        embed.set_image(url=json_bully_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
         embed = discord.Embed(title=f"You Bullied Yourself! )-(")
         embed.set_image(url="https://media.tenor.com/qlhSFpPh0Q8AAAAd/wassup-whats-up.gif")
         embed.set_footer(text="Next Time Mention A User To Bully Them :D")
         await ctx.send(embed=embed)


@commands.command(name="cuddle")
async def cuddle(ctx, member: commands.MemberConverter = None):
    if member:
        cuddler = requests.get("https://api.waifu.pics/sfw/cuddle")
        json_cuddle_data = json.loads(cuddler.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} cuddled {member.display_name}! ʕっ•ᴥ•ʔっ", color=discord.Color.dark_gray())
        embed.set_image(url=json_cuddle_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="You cuddled yourself! (づ｡◕‿‿◕｡)づ")
        embed.set_image(url="https://media.tenor.com/1vBnYuMNhPMAAAAS/bts-hug.gif")
        embed.set_footer(text="Next Time Mention A User To Cuddle Them :D")
        await ctx.send(embed=embed)


@commands.command(name="cry")
async def cry(ctx, member: commands.MemberConverter = None):
    if member:
        cryr = requests.get("https://api.waifu.pics/sfw/cry")
        json_cry_data = json.loads(cryr.text)
        embed = discord.Embed(title=f"{member.display_name} made {ctx.author.display_name} cry! (っ- ‸ – ς)", color=discord.Color.dark_gray())
        embed.set_image(url=json_cry_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} is crying! (っ- ‸ – ς)", color=discord.Color.dark_gray())
        embed.set_image(url="https://media.tenor.com/pRTPXrxI2UAAAAAS/crying-meme-black-guy-cries.gif")
        await ctx.send(embed=embed)


@commands.command(name="pat")
async def pat(ctx, member: commands.MemberConverter = None):
    if member:
        patr = requests.get("https://api.waifu.pics/sfw/pat")
        json_pat_data = json.loads(patr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} patted {member.display_name}! (づ｡◕‿‿◕｡)づ", color=discord.Color.dark_gray())
        embed.set_image(url=json_pat_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} patted themselves! (づ｡◕‿‿◕｡)づ", color=discord.Color.dark_gray())
        embed.set_image(url="https://media.tenor.com/WOKtiwXYGogAAAAC/you-did-good-self-love.gif")
        await ctx.send(embed=embed)

@commands.command(name="bonk")
async def bonk(ctx, member: commands.MemberConverter = None):
    if member:
        bonkr = requests.get("https://api.waifu.pics/sfw/bonk")
        json_bonk_data = json.loads(bonkr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} bonked {member.display_name}! (눈_눈)", color=discord.Color.dark_gray())
        embed.set_image(url=json_bonk_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="You bonked yourself! (눈_눈)")
        embed.set_image(url="https://media.tenor.com/qnL-0us4GjwAAAAS/hammer-bonk.gif")
        await ctx.send(embed=embed)

@commands.command(name="smug")
async def smug(ctx, member: commands.MemberConverter = None):
    if member:
        smugr = requests.get("https://api.waifu.pics/sfw/smug")
        json_smug_data = json.loads(smugr.text)
        embed = discord.Embed(title=f"{member.display_name} got smugged by {ctx.author.display_name}! (￣‿￣)", color=discord.Color.dark_gray())
        embed.set_image(url=json_smug_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} is smugging! (￣‿￣)", color=discord.Color.dark_gray())
        embed.set_image(url="https://tenor.com/view/anime-smug-gif-22677264")
        await ctx.send(embed=embed)




@commands.command(name="blush")
async def blush(ctx, member: commands.MemberConverter = None):
    if member:
        blushr = requests.get("https://api.waifu.pics/sfw/blush")
        json_blush_data = json.loads(blushr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} made {member.display_name} blush! (⁄ ⁄•⁄ω⁄•⁄ ⁄)", color=discord.Color.dark_gray())
        embed.set_image(url=json_blush_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} is blushing! (⁄ ⁄•⁄ω⁄•⁄ ⁄)", color=discord.Color.dark_gray())
        embed.set_image(url="https://media.tenor.com/C0h6HyoKLkEAAAAC/pepe-blush.gif")
        await ctx.send(embed=embed)


@commands.command(name="wave")
async def wave(ctx, member: commands.MemberConverter = None):
    if member:
        waver = requests.get("https://api.waifu.pics/sfw/wave")
        json_wave_data = json.loads(waver.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} waved to {member.display_name}! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", color=discord.Color.dark_gray())
        embed.set_image(url=json_wave_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} waved at themselves! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", color=discord.Color.dark_gray())
        embed.set_image(url="https://media.tenor.com/Qy5sUxL5phgAAAAC/forest-gump-wave.gif")
        await ctx.send(embed=embed)

@commands.command(name="handhold")
async def handhold(ctx, member: commands.MemberConverter = None):
    if member:
        handr = requests.get("https://api.waifu.pics/sfw/handhold")
        json_hand_data = json.loads(handr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} is holding hands with {member.display_name}! (づ｡◕‿‿◕｡)づ", color=discord.Color.dark_gray())
        embed.set_image(url=json_hand_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} is holding their own hand! (づ｡◕‿‿◕｡)づ", color=discord.Color.dark_gray())
        embed.set_image(url="https://media.tenor.com/Nfzei0rwvSsAAAAS/hands.gif")
        await ctx.send(embed=embed)

@commands.command(name="nom")
async def nom(ctx, member: commands.MemberConverter = None):
    if member:
        nomr = requests.get("https://api.waifu.pics/sfw/nom")
        json_nom_data = json.loads(nomr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} is nomming {member.display_name}'s head! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", color=discord.Color.dark_gray())
        embed.set_image(url=json_nom_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} is nomming their own head! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", color=discord.Color.dark_gray())
        embed.set_image(url="https://cdn.discordapp.com/emojis/749763703158734859.gif?size=128&quality=lossless")
        await ctx.send(embed=embed)

@commands.command(name="kill")
async def kill(ctx, member: commands.MemberConverter = None):
    if member:
        killr = requests.get("https://api.waifu.pics/sfw/kill")
        json_kill_data = json.loads(killr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} killed {member.display_name}! (⌐■_■)", color=discord.Color.dark_gray())
        embed.set_image(url=json_kill_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} killed themselves! (⌐■_■)", color=discord.Color.dark_gray())
        await ctx.send(embed=embed)

@commands.command(name="kick")
async def kick(ctx, member: commands.MemberConverter = None):
    if member:
        kickr = requests.get("https://api.waifu.pics/sfw/kick")
        json_kick_data = json.loads(kickr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} kicked {member.display_name}! (ง'̀-'́)ง", color=discord.Color.dark_gray())
        embed.set_image(url=json_kick_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} kicked themselves! (ง'̀-'́)ง", color=discord.Color.dark_gray())
        embed.set_image(url="https://media.tenor.com/yxpzAkL8ABoAAAAS/weeman-kickinghimself.gif")
        await ctx.send(embed=embed)                     

@commands.command(name="wink")
async def wink(ctx, member: commands.MemberConverter = None):
    if member:
        winkr = requests.get("https://api.waifu.pics/sfw/wink")
        json_wink_data = json.loads(winkr.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} winked at {member.display_name}! (◕‿↼)", color=discord.Color.dark_gray())
        embed.set_image(url=json_wink_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} winked at yourself! (◕‿↼)", color=discord.Color.dark_gray())
        await ctx.send(embed=embed)

@commands.command(name="poke")
async def poke(ctx, member: commands.MemberConverter = None):
    if member:
        poker = requests.get("https://api.waifu.pics/sfw/poke")
        json_poke_data = json.loads(poker.text)
        embed = discord.Embed(title=f"{ctx.author.display_name} poked {member.display_name}! (＾◡＾)っ", color=discord.Color.dark_gray())
        embed.set_image(url=json_poke_data['url'])
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.display_name} poked themselves! (＾◡＾)っ", color=discord.Color.dark_gray())
        embed.set_image(url="https://media.tenor.com/cVMA5TtZ_3oAAAAS/baymax-poke.gif")
        await ctx.send(embed=embed)

