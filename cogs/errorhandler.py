import discord
from discord.ext import commands
from acemeta import log
from lib.dbinterface import NoEntryError

async def setup(bot):
    await bot.add_cog(Errorhandler(bot))

class Errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title=f"", color=15774002)
            embed.set_author(name="Dir fehlen Berechtigungen",
                             icon_url="https://cdn.discordapp.com/emojis/1233093266916773991.webp")
            await ctx.reply(embed = embed, mention_author=False)

    @commands.Cog.listener()
    async def on_ready(self):
        log(f"[COGS] {__name__} is ready")

