import discord
from discord.ext import commands

from core.http import get_session
from core.logging import log_command

PURRBOT = "https://purrbot.site/api/img/sfw/{}/gif"
WAIFU = "https://api.waifu.pics/sfw/{}"


class Gifs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _send_gif(
        self,
        ctx: commands.Context,
        member: discord.Member | None,
        endpoint: str,
        targeted_title: str,
        alone_title: str,
        alone_gif: str | None = None,
    ):
        log_command(ctx)
        if member:
            session = await get_session()
            async with session.get(endpoint) as resp:
                data = await resp.json()
            url = data.get("link") or data.get("url")
            embed = discord.Embed(title=targeted_title, color=discord.Color.dark_gray())
            embed.set_image(url=url)
        else:
            embed = discord.Embed(title=alone_title)
            if alone_gif:
                embed.set_image(url=alone_gif)
        embed.set_footer(text="Thank You For Using Catto! :D")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="hug", description="Hug another member (or yourself) with a cute gif")
    async def hug(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            PURRBOT.format("hug"),
            f"{ctx.author.display_name} hugs {member.display_name if member else ''}! ❁◕ ‿ ◕❁",
            "You hugged yourself! ❁◕ ‿ ◕❁",
            "https://media.tenor.com/XEEmDlNSmEcAAAAM/spongebob-love.gif",
        )

    @commands.hybrid_command(name="slap", description="Slap another member with an anime gif")
    async def slap(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            PURRBOT.format("slap"),
            f"{ctx.author.display_name} slaps {member.display_name if member else ''}! ( ಥ۝ಥ )",
            "You slapped yourself! ( ಥ۝ಥ )",
            "https://media.tenor.com/rXAnv88yrFwAAAAM/anime-slapping-face.gif",
        )

    @commands.hybrid_command(name="kiss", description="Kiss another member with an anime gif")
    async def kiss(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            PURRBOT.format("kiss"),
            f"{ctx.author.display_name} kisses {member.display_name if member else ''}! (ᅌwᅌ)",
            "You can't kiss yourself! ( ಥ۝ಥ )",
        )

    @commands.hybrid_command(name="lick", description="Lick another member (gif)")
    async def lick(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            PURRBOT.format("lick"),
            f"{ctx.author.display_name} licks {member.display_name if member else ''}! (✿ ♥‿♥)",
            "You licked yourself! ♥‿♥",
            "https://media.tenor.com/6StCIWYFkOcAAAAC/adalfarus-adal.gif",
        )

    @commands.hybrid_command(name="bite", description="Bite another member (gif)")
    async def bite(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            PURRBOT.format("bite"),
            f"{ctx.author.display_name} bites {member.display_name if member else ''}! (ಥ۝ಥ)",
            "You bit yourself! ( ಥ۝ಥ )",
            "https://media.tenor.com/D7XNyUe6Q7UAAAAS/hit-self-kitten.gif",
        )

    @commands.hybrid_command(name="bully", description="Bully another member (gif)")
    async def bully(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("bully"),
            f"{ctx.author.display_name} bullied {member.display_name if member else ''}! (ಥ﹃ಥ)",
            "You bullied yourself!",
            "https://media.tenor.com/qlhSFpPh0Q8AAAAd/wassup-whats-up.gif",
        )

    @commands.hybrid_command(name="cuddle", description="Cuddle another member (gif)")
    async def cuddle(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("cuddle"),
            f"{ctx.author.display_name} cuddled {member.display_name if member else ''}! ʕっ•ᴥ•ʔっ",
            "You cuddled yourself! (づ｡◕‿‿◕｡)づ",
            "https://media.tenor.com/1vBnYuMNhPMAAAAS/bts-hug.gif",
        )

    @commands.hybrid_command(name="cry", description="Cry (gif) — optionally because of someone")
    async def cry(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("cry"),
            f"{member.display_name if member else ''} made {ctx.author.display_name} cry! (っ- ‸ – ς)",
            f"{ctx.author.display_name} is crying! (っ- ‸ – ς)",
            "https://media.tenor.com/pRTPXrxI2UAAAAS/crying-meme-black-guy-cries.gif",
        )

    @commands.hybrid_command(name="pat", description="Pat another member on the head (gif)")
    async def pat(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("pat"),
            f"{ctx.author.display_name} patted {member.display_name if member else ''}! (づ｡◕‿‿◕｡)づ",
            f"{ctx.author.display_name} patted themselves!",
            "https://media.tenor.com/WOKtiwXYGogAAAAC/you-did-good-self-love.gif",
        )

    @commands.hybrid_command(name="bonk", description="Bonk another member (gif)")
    async def bonk(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("bonk"),
            f"{ctx.author.display_name} bonked {member.display_name if member else ''}! (눈_눈)",
            "You bonked yourself! (눈_눈)",
            "https://media.tenor.com/qnL-0us4GjwAAAAS/hammer-bonk.gif",
        )

    @commands.hybrid_command(name="smug", description="Smug face (gif) at another member")
    async def smug(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("smug"),
            f"{member.display_name if member else ''} got smugged by {ctx.author.display_name}! (￣‿￣)",
            f"{ctx.author.display_name} is smugging! (￣‿￣)",
        )

    @commands.hybrid_command(name="blush", description="Blush (gif) — optionally because of someone")
    async def blush(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("blush"),
            f"{ctx.author.display_name} made {member.display_name if member else ''} blush! (⁄ ⁄•⁄ω⁄•⁄ ⁄)",
            f"{ctx.author.display_name} is blushing! (⁄ ⁄•⁄ω⁄•⁄ ⁄)",
            "https://media.tenor.com/C0h6HyoKLkEAAAAC/pepe-blush.gif",
        )

    @commands.hybrid_command(name="handhold", description="Hold hands with another member (gif)")
    async def handhold(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("handhold"),
            f"{ctx.author.display_name} is holding hands with {member.display_name if member else ''}!",
            f"{ctx.author.display_name} is holding their own hand!",
            "https://media.tenor.com/Nfzei0rwvSsAAAAS/hands.gif",
        )

    @commands.hybrid_command(name="nom", description="Nom another member's head (gif)")
    async def nom(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("nom"),
            f"{ctx.author.display_name} is nomming {member.display_name if member else ''}'s head!",
            f"{ctx.author.display_name} is nomming their own head!",
            "https://cdn.discordapp.com/emojis/749763703158734859.gif?size=128",
        )

    @commands.hybrid_command(name="kill", description="Kill another member (gif)")
    async def kill(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("kill"),
            f"{ctx.author.display_name} killed {member.display_name if member else ''}! (⌐■_■)",
            f"{ctx.author.display_name} killed themselves! (⌐■_■)",
        )

    @commands.hybrid_command(name="wink", description="Wink at another member (gif)")
    async def wink(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("wink"),
            f"{ctx.author.display_name} winked at {member.display_name if member else ''}! (◕‿↼)",
            f"{ctx.author.display_name} winked at themselves! (◕‿↼)",
        )

    @commands.hybrid_command(name="poke", description="Poke another member (gif)")
    async def poke(self, ctx: commands.Context, member: discord.Member | None = None):
        await self._send_gif(
            ctx,
            member,
            WAIFU.format("poke"),
            f"{ctx.author.display_name} poked {member.display_name if member else ''}! (＾◡＾)っ",
            f"{ctx.author.display_name} poked themselves! (＾◡＾)っ",
            "https://media.tenor.com/cVMA5TtZ_3oAAAAS/baymax-poke.gif",
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Gifs(bot))
