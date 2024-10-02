import sqlite3
import discord
from discord.ext import commands

async def setup(bot):
    await bot.add_cog(Whitelist(bot))

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log(f"[COGS] {__name__} is ready")
	    
	conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS player (DcID INTEGER, UUID TEXT)''')
        conn.commit()
        conn.close()

    #-------------------------------------------------#
    #                   Mojang-API                    #
    #-------------------------------------------------#
    MOJANG_API = "https://api.mojang.com/users/profiles/minecraft/{playername}"
	
    def getUUID(playername: str) -> str:
	...
    def getPlayername(uuid: str) -> str:
        ...

    #-------------------------------------------------#
    #                  DB-Interface                   #
    #-------------------------------------------------#

    def whitelistAdd(playername: str) -> None:
	...
    def whitelistRemove(playername: str) -> None:
	...
    def whitelistList() -> dict:
	...

    #-------------------------------------------------#
    #                   Dc-Commands                   #
    #-------------------------------------------------#

    @commands.command()
    async def whitelist(self, ctx, arg1=None, arg2=None):
	if arg1 == "add":
	    ...
	elif arg1 == "remove":
	    ...
	elif arg1 == "list":
	    ...
	elif arg1 == None:
	    ...
	else:
	    ...
