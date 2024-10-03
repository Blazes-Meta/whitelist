OPERATORS = [].append(720992368110862407)

import discord
from discord import app_commands
from discord.ext import commands
from lib.applib import *
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

    @app_commands.command(name="playerbase", description="Erstelle, Ändere oder Entferne einen EIntrag in der Playerbase")
    @app_commands.choices(aktion=[
        app_commands.Choice(name="Setzen", value="set"),
        app_commands.Choice(name="Entfernen", value="remove"),
        app_commands.Choice(name="Auflisten", value="list"),])
    
    async def playerbase(self, i: discord.Interaction, aktion: app_commands.Choice[str], discorduser: discord.User=None, minecraftname: str=None):

        #await i.response.send_message(f"User: {discorduser}, Action: {minecraftname}, Choice: {aktion.value}")

        dcid = discorduser.id
        authorid = i.user.id

        if aktion.value == "set": 
        # ╭────────────────────────────────────────────────────────────╮
        # │                            SET                             │ 
        # ╰────────────────────────────────────────────────────────────╯

            if dcid == authorid or authorid in OPERATORS:
                if minecraftname is not None:
                    playerbaseSet(dcid=dcid, playername=minecraftname)
                    await i.response.send_message(f"<@{dcid}> wurde mit {minecraftname} ({getUUID(minecraftname)}) verbunden")
                
                else:
                    #raise MissingArgument("Bitte gib einen Minecraftnamen an")
                    raise app_commands.AppCommandError

            else:
                #raise MissingPermissionsError
                raise app_commands.AppCommandError
        
        elif aktion.value == "remove": ...
        # ╭────────────────────────────────────────────────────────────╮
        # │                          REMOVE                            │ 
        # ╰────────────────────────────────────────────────────────────╯

        
        elif aktion.value == "list": ...
        # ╭────────────────────────────────────────────────────────────╮
        # │                           LIST                             │ 
        # ╰────────────────────────────────────────────────────────────╯