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
    await bot.add_cog(PlayerbaseCMD(bot))

class PlayerbaseCMD(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")

        
    #playerbase = app_commands.Group(name="playerbase", description="Nimm Änderungen an der Playerbase vor")

    
    # @app_commands.choices(aktion=[
    #     app_commands.Choice(name="set", value="set"),
    #     app_commands.Choice(name="delete", value="delete"),
    #     app_commands.Choice(name="get", value="get"),])
    
    # ╭────────────────────────────────────────────────────────────╮
    # │                            SET                             │ 
    # ╰────────────────────────────────────────────────────────────╯
    @app_commands.command(name="playerbaseset", description="Erstelle, Ändere oder Entferne einen Eintrag in der Playerbase")
    async def playerbaseSet(self, i: discord.Interaction, discorduser: discord.User, minecraft: str):

        dcid = discorduser.id
        authorid = i.user.id

        if dcid == authorid or authorid in OPERATORS:
            if minecraft is not None:
                
                try:
                    if len(minecraft) > 16:
                        uuid = minecraft.replace("-", "")
                        minecraftname = getPlayername(minecraft)
                    else:
                        uuid = getUUID(minecraft)
                        minecraftname = minecraft

                    pb.setPlayer(dcid=dcid, uuid=uuid)
                    try: repo.upload(file=PLAYERBASE_LOCAL, directory="data/playerbase.db", msg="Playerbase-Upload", overwrite=True)
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
                raise apps.MissingAppArgument("Bitte gib einen gültigen Minecraft-Namen an")

        else:
            raise apps.AppPermissionError(f"Du musst ein Operator oder <@{dcid}> sein, um diesen Eintrag ändern zu können")
            
    # ╭────────────────────────────────────────────────────────────╮
    # │                          REMOVE                            │ 
    # ╰────────────────────────────────────────────────────────────╯
        
    @app_commands.command(name="playerbasedelete", description="Entferne einen Eintrag aus der Playerbase")
    async def playerbaseDelete(self, i: discord.Interaction, discorduser: discord.User):
    
        dcid = discorduser.id
        authorid = i.user.id

        if (dcid == authorid) or (authorid in OPERATORS):
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
            try: repo.upload(file=PLAYERBASE_LOCAL, directory="data/playerbase.db", msg="Playerbase-Upload", overwrite=True)
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
    @app_commands.command(name="playerbaseget", description="Gibt einen Eintrag zurück")
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

    @app_commands.command(name="listplayerbase", description="Spuckt die gesammte Playerbase aus")
    async def playerbase_get(self, i: discord.Interaction):
        playerbase = pb.list()

        # Dieser wilde Code hier sortiert die User nach ihren Discordnamen, die ja aber in der Datenbank
        # eigentlich garnicht vorliegen
        users = []
        for key, value in playerbase.items():
            discorduser = self.bot.get_user(key)
            discordname = discorduser.display_name
            users.append([key, discordname, value])
        users = sorted(users, key=lambda x: x[1])
        strings = []

        for user in users:
            strings.append(f"<@{user[0]}> - {getPlayername(user[2])}")
        string = "\n".join(strings)

        if len(string) == 0:
            string = "Keine Einträge vorhanden"

        embed = discord.Embed(title="Playerbase",
                              description=string,
                              color=3908961)
        await i.response.send_message(embed = embed)
