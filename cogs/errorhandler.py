import discord
from discord import app_commands
from discord.ext import commands
from lib.dbinterface import NoEntryError
from lib.apps import *

async def setup(bot):
    await bot.add_cog(Errorhandler(bot))

class Errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")

    # ╭────────────────────────────────────────────────────────────╮
    # │           app_command Error Handeler Workaround            │ 
    # ╰────────────────────────────────────────────────────────────╯
    # Jo also dieser Workaround ist vom discord.py Discord. App Commands sind echt be******en.
    # Aber hey, es funktioniert auch für Kontextmenüs

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.tree_on_error # 3rd line <-

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    async def tree_on_error(self, i: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingArgument):
            embed = discord.Embed(title=f"{str(error)}", color=15774002)
            embed.set_author(name="Es fehlt ein Argument",
                             icon_url="https://cdn.discordapp.com/emojis/1233093266916773991.webp")
            await i.response.send_message(embed = embed, ephemeral=True)
        
        else:
            await i.response.send_message("Es ist ein Fehler aufgetreten")

    # ╭────────────────────────────────────────────────────────────╮
    # │            discord.ext command error Handeler              │ 
    # ╰────────────────────────────────────────────────────────────╯

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=f"{error}", color=15774002)
            embed.set_author(name="Ein Argument entsprach nicht den Erwartungen",
                             icon_url="https://cdn.discordapp.com/emojis/1233093266916773991.webp")
            await ctx.reply(embed = embed, mention_author=False)
        
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=f"", color=15774002)
            embed.set_author(name="Es muss ein weiteres Argument angegeben werden.",
                             icon_url="https://cdn.discordapp.com/emojis/1233093266916773991.webp")
            await ctx.reply(embed = embed, mention_author=False)

        elif isinstance(error, NoEntryError):
            embed = discord.Embed(title=f"{error}", color=15774002)
            embed.set_author(name="Es wurde kein Eintrag in der Playerbase gefunden",
                             icon_url="https://cdn.discordapp.com/emojis/1233093266916773991.webp")
            await ctx.reply(embed = embed, mention_author=False)