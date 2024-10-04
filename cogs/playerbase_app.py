OPERATORS = [].append(720992368110862407)

import discord
from discord import app_commands
from discord.ext import commands
from lib.apps import *
from lib.mojang import *
from lib.dbinterface import *

async def setup(bot):
    await bot.add_cog(PlayerbaseApp(bot))

class PlayerbaseApp(commands.Cog):
    def __init__(self, bot):
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

        if aktion.value == "set": 
        # ╭────────────────────────────────────────────────────────────╮
        # │                            SET                             │ 
        # ╰────────────────────────────────────────────────────────────╯
            
            if dcid == authorid or authorid in OPERATORS:
                if minecraftname is not None:
                    self.pb.playerbaseSet(dcid=dcid, playername=minecraftname)
                    await i.response.send_message(f"<@{dcid}> wurde mit {minecraftname} ({getUUID(minecraftname)}) verbunden")
                
                else:
                    raise MissingAppArgument("Bitte gib einen Minecraftnamen an")

            else:
                raise AppPermissionError
            
            
        
        elif aktion.value == "delete":
        # ╭────────────────────────────────────────────────────────────╮
        # │                          REMOVE                            │ 
        # ╰────────────────────────────────────────────────────────────╯

            if dcid == authorid or authorid in OPERATORS:
                self.pb.playerbaseRemove(dcid=dcid)
                await i.response.send_message(f"<@{dcid}> wurde aus der Playerbase entfernt")

            else:
                raise AppPermissionError
                
        
        elif aktion.value == "get":
        # ╭────────────────────────────────────────────────────────────╮
        # │                           LIST                             │ 
        # ╰────────────────────────────────────────────────────────────╯

            uuid = self.pb.playerbaseGet(dcid)
            name = getPlayername(uuid)
            await i.response.send_message(f"<@{dcid}> ist aktuell mit {name} verbunden")