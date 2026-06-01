import io
from pathlib import Path

import discord
from PIL import Image, ImageDraw, ImageFont

CARD_W, CARD_H = 900, 300
AVATAR_SIZE = 200
PADDING = 50

FONT_CANDIDATES = [
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def _font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _circle_crop(img: Image.Image, size: int) -> Image.Image:
    img = img.resize((size, size)).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def _gradient_background() -> Image.Image:
    bg = Image.new("RGB", (CARD_W, CARD_H), (28, 30, 40))
    top = (44, 47, 80)
    bot = (28, 30, 40)
    for y in range(CARD_H):
        t = y / CARD_H
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        ImageDraw.Draw(bg).line([(0, y), (CARD_W, y)], fill=(r, g, b))
    return bg.convert("RGBA")


async def render_welcome_card(
    member: discord.Member, headline: str = "Welcome!", subline: str | None = None
) -> bytes:
    canvas = _gradient_background()
    avatar_bytes = await member.display_avatar.replace(size=256).read()
    avatar = _circle_crop(Image.open(io.BytesIO(avatar_bytes)), AVATAR_SIZE)
    # Outline ring around the avatar
    ring = Image.new("RGBA", (AVATAR_SIZE + 12, AVATAR_SIZE + 12), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse(
        (0, 0, AVATAR_SIZE + 12, AVATAR_SIZE + 12), fill=(255, 255, 255, 220)
    )
    canvas.paste(ring, (PADDING - 6, PADDING - 6), ring)
    canvas.paste(avatar, (PADDING, PADDING), avatar)

    draw = ImageDraw.Draw(canvas)
    text_x = PADDING + AVATAR_SIZE + 40
    draw.text((text_x, 60), headline, font=_font(56), fill=(255, 255, 255))
    draw.text((text_x, 130), str(member), font=_font(34), fill=(220, 220, 220))
    if subline is None:
        subline = f"You are member #{member.guild.member_count}"
    draw.text((text_x, 185), subline, font=_font(24), fill=(170, 170, 200))
    draw.text((text_x, 225), member.guild.name, font=_font(20), fill=(130, 130, 160))

    buf = io.BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


async def render_leave_card(member: discord.Member) -> bytes:
    canvas = _gradient_background()
    avatar_bytes = await member.display_avatar.replace(size=256).read()
    avatar = _circle_crop(Image.open(io.BytesIO(avatar_bytes)), AVATAR_SIZE)
    canvas.paste(avatar, (PADDING, PADDING), avatar)
    draw = ImageDraw.Draw(canvas)
    text_x = PADDING + AVATAR_SIZE + 40
    draw.text((text_x, 70), "Goodbye!", font=_font(56), fill=(220, 110, 110))
    draw.text((text_x, 140), str(member), font=_font(34), fill=(220, 220, 220))
    draw.text((text_x, 195), "Thanks for stopping by.", font=_font(22), fill=(170, 170, 200))
    buf = io.BytesIO()
    canvas.convert("RGB").save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()
