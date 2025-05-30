import discord
from discord import app_commands
from discord.ext import commands
import lib.apps as apps
from lib.mojang import *
from lib.dbinterface import *
from lib.github import Repository
from dotenv import load_dotenv
from yaml import load, SafeLoader
import os

# ╭────────────────────────────────╮
# │              ENV               │ 
# ╰────────────────────────────────╯

with open("config.yaml", "r") as config:
    config = load(config, Loader=SafeLoader)

OPERATORS = config["permissions"]["operators"]
LOCAL_PATH = config["database"]["local-path"]
REPOSITORY = config["github"]["repository"]
GITHUB_PATH = config["database"]["github-path"]

load_dotenv()

repo = Repository(repository=REPOSITORY, token=os.getenv("GITHUB_TOKEN"))
pb = Playerbase(dbpath=LOCAL_PATH)

# ╭────────────────────────────────╮
# │              Cog               │ 
# ╰────────────────────────────────╯

async def setup(bot):
    await bot.add_cog(PlayerbaseCMD(bot))

class PlayerbaseCMD(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_cache = {}
        self.playername_cache = {}
        
    playerbase = app_commands.Group(name="playerbase", description="Nimm Änderungen an der Playerbase vor")

        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")

        repo.download(file="data/playerbase.db", destination=pb.dbpath, overwrite=True)

    # ╭────────────────────────────────────────────────────────────╮
    # │                            SET                             │ 
    # ╰────────────────────────────────────────────────────────────╯
    @playerbase.command(name="set", description="Verbinde einen Discord-Nutzer mit Minecraft")
    async def playerbaseSet(self, i: discord.Interaction, discorduser: discord.User, minecraft: str):

        dcid = discorduser.id
        interactorid = i.user.id

        if dcid == interactorid or interactorid in OPERATORS:
            try:
                if len(minecraft) > 16:
                    uuid = minecraft.replace("-", "")
                    minecraftname = getPlayername(minecraft)
                else:
                    uuid = getUUID(minecraft)
                    minecraftname = minecraft

                pb.setPlayer(dcid=dcid, uuid=uuid)

                try: repo.upload(file=LOCAL_PATH, directory=GITHUB_PATH, msg="Playerbase-Upload", overwrite=True)
                except Exception as e: raise apps.GithubError(str(e))

                embed = discord.Embed(title="",
                                      description=f"<@{dcid}> wurde mit <:mc:1291359572614844480> **{minecraftname}** verbunden\n-# UUID: `{uuid}`",
                                      color=3908961)
                embed.set_author(name="Ein Discord-Nutzer wurde mit Minecraft verbunden",
                                 icon_url="https://cdn.discordapp.com/emojis/1291772994250866720.webp")
                embed.set_footer(text=f"/playerbase set @{discorduser.name} {minecraftname}",
                                 icon_url=i.user.avatar)
                embed.set_thumbnail(url=f"https://mineskin.eu/helm/{minecraftname}/100.png")
                await i.response.send_message(embed = embed)

            except MojangAPIError:
                raise apps.AppAPIError(f"{minecraft} ist kein gültiger Minecraft-Account")

        else:
            raise apps.AppPermissionError(f"Du musst ein Operator oder <@{dcid}> sein, um diesen Eintrag ändern zu können")
            
    # ╭────────────────────────────────────────────────────────────╮
    # │                          REMOVE                            │ 
    # ╰────────────────────────────────────────────────────────────╯
        
    @playerbase.command(name="delete", description="Entferne einen Eintrag aus der Playerbase")
    async def playerbaseDelete(self, i: discord.Interaction, discorduser: discord.User):
    
        dcid = discorduser.id
        cmduser = i.user.id

        if dcid == cmduser or cmduser in OPERATORS:
            try:
                minecraftname = getPlayername(pb.getPlayerUUID(dcid))
            except NoEntryError:
                embed = discord.Embed(title="",
                                        description=f"<@{dcid}> ist aktuell mit keinem Minecraft-Account verbunden",
                                        color=15284296)
                embed.set_author(name="Kein Eintrag gefunden",
                                    icon_url="https://cdn.discordapp.com/emojis/1291775670975729716.webp")
                await i.response.send_message(embed = embed)

            pb.removePlayer(dcid=dcid)

            try: repo.upload(file=LOCAL_PATH, directory=GITHUB_PATH, msg="Playerbase-Upload", overwrite=True)
            except Exception as e: raise apps.GithubError(str(e))
            
            embed = discord.Embed(title="",
                                  description=f"<@{dcid}>s Verbindung mit <:mc:1291359572614844480> **{minecraftname}** wurde aufgehoben\n-# UUID: `{getUUID(minecraftname)}`",
                                  color=3908961)
            embed.set_author(name="Der Eintrag eines Discord-Nutzers wurde entfernt",
                             icon_url="https://cdn.discordapp.com/emojis/1291772994250866720.webp")
            embed.set_footer(text=f"/playerbase remove @{discorduser.name}",
                             icon_url=i.user.avatar)
            await i.response.send_message(embed = embed)

        else:
            raise apps.AppPermissionError(f"Du musst ein Operator oder <@{dcid}> sein, um diesen Eintrag löschen zu können")
            

        
    # ╭────────────────────────────────────────────────────────────╮
    # │                            GET                             │ 
    # ╰────────────────────────────────────────────────────────────╯

    @playerbase.command(name="get", description="Sieh nach, mit welchem Minecraft-Account ein Nutzer verbunden ist")
    async def playerbaseGet(self, i: discord.Interaction, discorduser: discord.User):
        
        dcid = discorduser.id

        try:
            uuid = pb.getPlayerUUID(dcid)
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

        await i.response.send_message(embed = embed)
            

    # ╭────────────────────────────────────────────────────────────╮
    # │                           LIST                             │ 
    # ╰────────────────────────────────────────────────────────────╯

    @playerbase.command(name="list", description="Spuckt die gesamte Playerbase aus")
    async def playerbase_get(self, i: discord.Interaction):
        await i.response.defer()

        playerbase = pb.listEntries()

        # Dieser wilde Code hier sortiert die User nach ihren Discordnamen, die ja aber in der Datenbank
        # eigentlich garnicht vorliegen
        users = []
        for key, value in playerbase.items():
            # Überprüfe, ob der User bereits im Cache ist
            if key not in self.user_cache:
                discorduser = self.bot.get_user(key)
                try: # Soll einen Bug fixen, bei dem kein User gefundedn wird
                    self.user_cache[key] = discorduser.display_name
                except:
                    self.user_cache[key] = "zzz" # SOrgt dafür, dass die dann ganz unten einsortiert werden
            discordname: str = self.user_cache[key]
            users.append([key, discordname.lower(), value])
        
        users = sorted(users, key=lambda x: x[1])
        strings = []

        for user in users:
            if user[0] not in self.playername_cache:
                self.playername_cache[user[0]] = getPlayername(user[2])
            playername = self.playername_cache[user[0]]
            strings.append(f"<@{user[0]}> - {discord.utils.escape_markdown(playername)}")

        string = "\n".join(strings)

        if len(string) == 0:
            string = "Keine Einträge vorhanden"

        embed = discord.Embed(
            title="Playerbase",
            description="-# Aufgrund von Caching könnten die Spielernamen veraltet sein\n\n" + string,
            color=3908961
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1291359572614844480.webp")

        await i.followup.send(embed=embed)
