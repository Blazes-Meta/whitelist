OPERATORS: list[int] = [].append(720992368110862407)

import discord
from discord import app_commands
from discord.ext import commands
import lib.apps as apps
from lib.mojang import *
from lib.dbinterface import *

async def setup(bot):
    await bot.add_cog(PlayerbaseApp(bot))

class PlayerbaseApp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")

        self.pb = Playerbase(dbpath="playerbase.db")

    @app_commands.command(name="playerbase", description="Erstelle, Ändere oder Entferne einen EIntrag in der Playerbase")
    @app_commands.choices(aktion=[
        app_commands.Choice(name="set", value="set"),
        app_commands.Choice(name="delete", value="delete"),
        app_commands.Choice(name="get", value="get"),])
    
    async def playerbase(self, i: discord.Interaction, aktion: app_commands.Choice[str], discorduser: discord.User, minecraftname: str=None):

        dcid = discorduser.id
        authorid = i.user.id
        #print(authorid)

        if aktion.value == "set": 
        # ╭────────────────────────────────────────────────────────────╮
        # │                            SET                             │ 
        # ╰────────────────────────────────────────────────────────────╯
            
            if dcid == authorid or authorid in OPERATORS:
                if minecraftname is not None:
                    try:
                        self.pb.setPlayer(dcid=dcid, uuid=getUUID(minecraftname))
                        embed = discord.Embed(title="",
                                            description=f"<@{dcid}> wurde mit <:mc:1291359572614844480> **{minecraftname}** verbunden\n-# UUID: `{getUUID(minecraftname)}`",
                                            color=3908961)
                        embed.set_author(name="Ein Discord-Nutzer wurde mit Minecraft verbunden",
                                         icon_url="https://cdn.discordapp.com/emojis/1291772994250866720.webp")
                        embed.set_footer(text=f"/playerbase set @{discorduser.name} {minecraftname}",
                                         icon_url=i.user.avatar)
                        embed.set_thumbnail(url=f"https://mineskin.eu/helm/{minecraftname}/100.png")
                        await i.response.send_message(embed = embed)

                    except APIError as e:
                        raise apps.AppAPIError(f"{minecraftname} ist kein gültiger Minecraft-Account")
                
                else:
                    raise MissingAppArgument("Bitte gib einen Minecraftnamen an")

            else:
                raise apps.AppPermissionError(f"Du musst ein Operator oder <@{dcid}> sein, um diesen Eintrag ändern zu können")
            
            
        
        elif aktion.value == "delete":
        # ╭────────────────────────────────────────────────────────────╮
        # │                          REMOVE                            │ 
        # ╰────────────────────────────────────────────────────────────╯

            if dcid == authorid or authorid in OPERATORS:
                minecraftname = getPlayername(self.pb.getPlayerUUID(dcid))
                self.pb.removePlayer(dcid=dcid)
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
                

        
        elif aktion.value == "get":
        # ╭────────────────────────────────────────────────────────────╮
        # │                           LIST                             │ 
        # ╰────────────────────────────────────────────────────────────╯

            uuid = self.pb.getPlayerUUID(dcid)
            minecraftname = getPlayername(uuid)
            embed = discord.Embed(title="Playerbase-Einsicht",
                                  description=f"<@{dcid}> ist aktuell mit <:mc:1291359572614844480> **{minecraftname}** verbunden\n-# UUID: `{getUUID(minecraftname)}`",
                                  color=3908961)
            embed.set_thumbnail(url=f"https://mineskin.eu/helm/{minecraftname}/100.png")
            await i.response.send_message(embed = embed)



    @app_commands.command(name="playerbaselist", description="Spuckt die gesammte Playerbase aus")
    async def playerbase_get(self, i: discord.Interaction):
        playerbase = self.pb.list()
        users = []
        for key, value in playerbase.items():
            discorduser = await self.bot.get_user(key)
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
        # embed.set_author(name="Der Eintrag eines Discord-Nutzers wurde entfernt",
        #                     icon_url="https://cdn.discordapp.com/emojis/1291772994250866720.webp")
        # embed.set_footer(text=f"/playerbase remove @{discorduser.name}",
        #                     icon_url=f"https://mineskin.eu/helm/{minecraftname}/100.png")
        await i.response.send_message(embed = embed)