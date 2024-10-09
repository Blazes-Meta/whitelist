OPERATORS: list[int] = [720992368110862407] #
PLAYERBASE_LOCAL = "tmp/playerbase.db"

import discord
from discord import app_commands
from discord.ext import commands
import lib.apps as apps
from lib.mojang import *
from lib.dbinterface import *
from lib.github import Repository
from dotenv import load_dotenv
import os

# ╭────────────────────────────────╮
# │              ENV               │ 
# ╰────────────────────────────────╯

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
repo = Repository(repository="annhilati/whitelist", token=GITHUB_TOKEN)

pb = Playerbase(dbpath=PLAYERBASE_LOCAL)

# ╭────────────────────────────────╮
# │              Cog               │ 
# ╰────────────────────────────────╯

async def setup(bot):
    await bot.add_cog(WhitelistCMD(bot))



class WhitelistCMD(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #self.user_cache = {}
        
    whitelist = app_commands.Group(name="whitelist", description="Nimm Änderungen an der Whitelist vor")

        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")

            
    # ╭────────────────────────────────────────────────────────────╮
    # │                            ADD                             │ 
    # ╰────────────────────────────────────────────────────────────╯
        
    @whitelist.command(name="add", description="Entferne einen Eintrag aus der Playerbase")
    async def whitelistAdd(self, i: discord.Interaction, discorduser: discord.User):
        
        dcid = discorduser.id
        registered = pb.entryExists(dcid)
        authorid = i.user.id

        if authorid in OPERATORS:
            try:
                pb.whitelistAdd(dcid)
            except sqlite3.IntegrityError:
                raise apps.AlreadyExists

            try: repo.upload(file=PLAYERBASE_LOCAL, directory="data/playerbase.db", msg="Playerbase-Upload", overwrite=True)
            except Exception as e: raise apps.GithubError(str(e))

            if registered:
                uuid = pb.getPlayerUUID(dcid)
                minecraftname = getPlayername(uuid)

                embed = discord.Embed(title="",
                                    description=f"<@{dcid}> wurde als <:mc:1291359572614844480> **{minecraftname}** zur Whitelist hinzugefügt\n-# UUID: `{uuid}`",
                                    color=3908961)
                embed.set_author(name="Ein Spieler wurde zur Whitelist hinzugefügt",
                                icon_url="https://cdn.discordapp.com/emojis/1291772994250866720.webp")
                embed.set_footer(text=f"/whitelist add @{discorduser.name}",
                                icon_url=i.user.avatar)
                embed.set_thumbnail(url=f"https://mineskin.eu/helm/{minecraftname}/100.png")

            else:
                embed = discord.Embed(title="",
                                    description=f"<@{dcid}> wurde zur Whitelist hinzugefügt\n-# Dieser Account ist noch nicht mit Minecraft verknüpft. Nutze `/playerbase set` um dies zu tun.",
                                    color=3908961)
                embed.set_author(name="Ein Spieler wurde zur Whitelist hinzugefügt",
                                icon_url="https://cdn.discordapp.com/emojis/1291772994250866720.webp")
                embed.set_footer(text=f"/whitelist add @{discorduser.name}",
                                icon_url=i.user.avatar)
            
            await i.response.send_message(embed = embed)

        else:
            raise apps.AppPermissionError(f"Du musst ein Operator sein, um diesen Eintrag ändern zu können")
        
    # ╭────────────────────────────────────────────────────────────╮
    # │                           REMOVE                           │ 
    # ╰────────────────────────────────────────────────────────────╯
    @whitelist.command(name="delete", description="Gibt einen Eintrag zurück")
    async def whitelistRemove(self, i: discord.Interaction, discorduser: discord.User):
        
        dcid = discorduser.id
        whitelisted = pb.isonWhitelist(dcid)
        authorid = i.user.id

        if authorid in OPERATORS:   
            if whitelisted:

                pb.whitelistRemove(dcid)

                embed = discord.Embed(title="",
                                    description=f"<@{dcid}> wurde von der Whitelist gestrichen",
                                    color=3908961)
                embed.set_author(name="Ein Spieler wurde aus der Whitelist entfernt",
                                icon_url="https://cdn.discordapp.com/emojis/1291772994250866720.webp")
                embed.set_footer(text=f"/whitelist add @{discorduser.name}",
                                icon_url=i.user.avatar)

            else:
                raise apps.DoesntExist
                
            try: repo.upload(file=PLAYERBASE_LOCAL, directory="data/playerbase.db", msg="Playerbase-Upload", overwrite=True)
            except Exception as e: raise apps.GithubError(str(e))
            
            await i.response.send_message(embed = embed)

        else:
            raise apps.AppPermissionError(f"Du musst ein Operator sein, um diesen Eintrag ändern zu können")
            

    # ╭────────────────────────────────────────────────────────────╮
    # │                           LIST                             │ 
    # ╰────────────────────────────────────────────────────────────╯

    @whitelist.command(name="list", description="Spuckt die gesamte Playerbase aus")
    async def whitelistList(self, i: discord.Interaction):
        ...