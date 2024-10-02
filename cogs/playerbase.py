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
        cursor.execute('CREATE TABLE IF NOT EXISTS player (DcID INTEGER PRIMARY KEY, UUID TEXT)')
        conn.commit()
        conn.close()

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
        return None
	    
    def getPlayername(uuid: str) -> str:
        response = requests.get(f"{MOJANG_SESSIONSERVER}/{uuid}")
        if response.status_code == 200:
            data = response.json()
            return data['name']
        return None

    #-------------------------------------------------#
    #                  DB-Interface                   #
    #-------------------------------------------------#

    def playerExists(DcID: int) -> bool:
	conn = sqlite3.connect('playerbase.db')
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM player WHERE DcID = ?", (DcID,))
        result = cursor.fetchone()
	conn.close()
	if result is None
            return False
	return True

    def playerbaseSet(DcID: int, playername: str) -> None:
	
	    
    def playerbaseRemove(DcID: str) -> None:
	...
	    
    def playerbaseList() -> dict:
	...
	    

    #-------------------------------------------------#
    #                   Dc-Commands                   #
    #-------------------------------------------------#

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
		
