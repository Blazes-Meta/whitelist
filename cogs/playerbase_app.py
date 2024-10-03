import discord
from discord import app_commands
from discord.ext import commands
from typing import List

async def setup(bot):
    await bot.add_cog(PlayerbaseApp(bot))

class PlayerbaseApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")

    @app_commands.command(name="playerbase")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Setzen", value="set"),
        app_commands.Choice(name="Entfernen", value="remove"),
        app_commands.Choice(name="Auflisten", value="list"),])
    async def playerbase(self, i: discord.Interaction, choices: app_commands.Choice[str]):
        
        if (choices.value == 'rock'):
            counter = 'paper'
        elif (choices.value == 'paper'):
            counter = 'scissors'
        else:
            counter = 'rock'
        # rest of your command