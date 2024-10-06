import discord
from discord import app_commands
from discord.ext import commands
from lib.mojang import *
from lib.dbinterface import *

async def setup(bot):
    await bot.add_cog(PlayerbaseCTXM(bot))

class PlayerbaseCTXM(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.pb = Playerbase(dbpath="playerbase.db")

        # Um Kontextmenüs in Cogs funktionieren zu lassen ist dieser abgefahrene Workaround nötig
        self.ctx_menu = app_commands.ContextMenu(
            name='Minecraft-Verbindung anzeigen',
            callback=self.user_details)
        self.bot.tree.add_command(self.ctx_menu)


    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")


    @app_commands.guild_only()
    async def user_details(self, i: discord.Interaction, member: discord.Member) -> None:

        dcid = member.id
        
        try:
            uuid = self.pb.getPlayerUUID(dcid)
            minecraftname = getPlayername(uuid)
            embed = discord.Embed(title="Playerbase-Einsicht",
                                description=f"<@{dcid}> ist aktuell mit <:mc:1291359572614844480> **{minecraftname}** verbunden\n-# UUID: `{getUUID(minecraftname)}`",
                                color=3908961)
            embed.set_thumbnail(url=f"https://mineskin.eu/helm/{minecraftname}/100.png")
            

        except NoEntryError:
            embed = discord.Embed(title="",
                                description=f"<@{dcid}> ist aktuell mit keinem Minecraft-Account verbunden",
                                color=15284296)
            embed.set_author(name="Kein Eintrag gefunden",
                                icon_url="https://cdn.discordapp.com/emojis/1291775670975729716.webp")

        await i.response.send_message(embed = embed, ephemeral=True)