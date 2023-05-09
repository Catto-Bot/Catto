import discord


def WIP():
    return discord.Embed(title="⏲ This feature is work in progress!",
                         description="It will sonn be available!!", color=0x89CFF0)


def permission_denied():
    return discord.Embed(title="🛑 Permission Denied!", description="You do not have permission to do this!",
                         color=0xFF0000)



def downloading():
    return discord.Embed(title="⏱ Downloading File...", description="Please wait for up to 3 seconds!",
                         color=0xFF0000)


def error(e="executing command"):
    return discord.Embed(title=f"⚠ Unknown error occurred while {e}!",
                         description="Please report to [Teapot.py](https://github.com/RedCokeDevelopment/Teapot.py) developers [here](https://github.com/RedCokeDevelopment/Teapot.py/issues)!",
                         color=0xFF0000)


