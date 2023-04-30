import discord
from discord.ext import commands

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Send Message", style=discord.ButtonStyle.red)
    async def menu1(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.send_message("Hello")

@commands.command(name="button")
async def button(ctx):
    view = Menu()
    await ctx.reply(view=view)
