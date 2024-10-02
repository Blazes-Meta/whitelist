import sqlite3
import discord
from discord.ext import commands

async def setup(bot):
    await bot.add_cog(Playerbase(bot))

class Playerbase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log(f"[COGS] {__name__} is ready")
	    
	conn = sqlite3.connect('playerbase.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS player (DcID INTEGER PRIMARY KEY, UUID TEXT NOT NULL)')
        conn.commit()
        conn.close()

    #-------------------------------------------------#
    #                   Mojang-API                    #
    #-------------------------------------------------#
    MOJANG_API = "https://api.mojang.com/users/profiles/minecraft"
    MOJANG_SESSIONSERVER = f"https://sessionserver.mojang.com/session/minecraft/profile"

    class APIError(Exception): ...
	
    def getUUID(playername: str) -> str:
	response = requests.get(f"{MOJANG_API}/{playername}")
	if response.status_code == 200:
            data = response.json()
            return data['id']
        raise APIError
	    
    def getPlayername(uuid: str) -> str:
        response = requests.get(f"{MOJANG_SESSIONSERVER}/{uuid}")
        if response.status_code == 200:
            data = response.json()
            return data['name']
        raise APIError

    #-------------------------------------------------#
    #                  DB-Interface                   #
    #-------------------------------------------------#

    class NoEntry(Exception): ...

    def playerExists(dcid: int) -> bool:
	conn = sqlite3.connect('playerbase.db')
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM player WHERE DcID = ?", (dcid,))
        result = cursor.fetchone()
	conn.close()
	if result is None
            return False
	return True

    def playerbaseSet(dcid: int, playername: str) -> None:
	uuid = getUUID(playername)
	if not playerExists(DcID):
	    conn = sqlite3.connect('playerbase.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO player (DcID, UUID) VALUES (?, ?)", (dcid, uuid))
	    conn.commit()
	    conn.close()
	else:
	    conn = sqlite3.connect('playerbase.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE player SET UUID = ? WHERE DcID = ?", (uuid, dcid))
	    conn.commit()
	    conn.close()
	    
    def playerbaseRemove(dcid: int) -> None:
	if playerExists(dcid):
	    conn = sqlite3.connect('playerbase.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM player WHERE DcID = ?", (dcid,)
	    conn.commit()
	    conn.close()
	else:
	    raise NoEntry
	    
    def playerbaseList() -> dict:
	...
	    

    #-------------------------------------------------#
    #                   Dc-Commands                   #
    #-------------------------------------------------#

    class PermissionError(Exception): ...

    @commands.command()
    async def playerbase(self, ctx, arg1=None, arg2=None):
	if arg1 == "set":
	    ...
		
	elif arg1 == "remove":
	    ...
		
	elif arg1 == "list":
	    ...
		
	elif arg1 == None:
	    ...
		
	else:
	    ...
		
