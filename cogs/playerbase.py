OPERATORS = [720992368110862407]
DATABASE = 'playerbase.db'

import sqlite3
import requests
import discord
from discord.ext import commands

async def setup(bot):
    await bot.add_cog(Playerbase(bot))

class Playerbase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")
	    
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS player (DcID INTEGER PRIMARY KEY, UUID TEXT NOT NULL)')
        conn.commit()
        conn.close()

    @commands.command()
    async def playerbase(self, ctx, arg1=None, arg2=None, arg3=None):

        #-------------------------------------------------#
        #                   Mojang-API                    #
        #-------------------------------------------------#
        MOJANG_API = "https://api.mojang.com/users/profiles/minecraft"
        MOJANG_SESSIONSERVER = f"https://sessionserver.mojang.com/session/minecraft/profile"
        
        def getUUID(playername: str) -> str:
            response = requests.get(f"{MOJANG_API}/{playername}")
            if response.status_code == 200:
                data = response.json()
                return data['id']
            raise Exception("UUID konnte nicht erhalten werden")
            
        def getPlayername(uuid: str) -> str:
            response = requests.get(f"{MOJANG_SESSIONSERVER}/{uuid}")
            if response.status_code == 200:
                data = response.json()
                return data['name']
            raise Exception("Spielername konnte nicht erhalten werden")

        #-------------------------------------------------#
        #                  DB-Interface                   #
        #-------------------------------------------------#

        def playerExists(dcid: int) -> bool:
            conn = sqlite3.connect('playerbase.db')
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM player WHERE DcID = ?", (dcid,))
            result = cursor.fetchone()
            conn.close()
            if result is None:
                return False
            return True

        def playerbaseSet(dcid: int, playername: str) -> None:
            uuid = getUUID(playername)
            conn = sqlite3.connect('playerbase.db')
            cursor = conn.cursor()
            if not playerExists(dcid):
                cursor.execute("INSERT INTO player (DcID, UUID) VALUES (?, ?)", (dcid, uuid))
            else:
                cursor.execute("UPDATE player SET UUID = ? WHERE DcID = ?", (uuid, dcid))
            conn.commit()
            conn.close()
            
        def playerbaseRemove(dcid: int) -> None:
            if playerExists(dcid):
                conn = sqlite3.connect('playerbase.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM player WHERE DcID = ?", (dcid,))
                conn.commit()
                conn.close()
            else:
                raise Exception("Kein Spieler vorhanden")
            
        def playerbaseList() -> dict:
            ...
	    

        #-------------------------------------------------#
        #                   Dc-Commands                   #
        #-------------------------------------------------#

        userid = ctx.author.id
        await ctx.message.add_reaction("✅")
            
        if arg1 == "set":
            if arg2 == userid or userid in OPERATORS:
                if arg3 is not None:
                    try:
                        playerbaseSet(dcid=arg2, playername=arg3)
                        await ctx.message.add_reaction("✅")
                    except Exception:
                        raise commands.BadArgument("playerbase set fehlgeschlagen")
                else:
                    raise commands.MissingRequiredArgument
            else:
                raise commands.PermissionError
            
        elif arg1 == "remove":
            if arg2 == userid or userid in OPERATORS:
                try:
                    playerbaseRemove(dcid=arg2)
                except Exception:
                    raise commands.BadArgument("playerbase remove fehlgeschlagen")
            else:
                raise commands.PermissionError
            
        elif arg1 == "list":
            ...
            
        elif arg1 == None:
            raise commands.MissingRequiredArgument
            
        else:
            raise commands.BadArgument
		
