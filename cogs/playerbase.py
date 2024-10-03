OPERATORS = [720992368110862407]
DATABASE = 'playerbase.db'

import sqlite3
import discord
from discord.ext import commands
from lib.dbinterface import *

async def setup(bot):
    await bot.add_cog(Playerbase(bot))

class Playerbase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")
	    
        initiatePlayerbase(DATABASE)

    #-------------------------------------------------#
    #                   Dc-Command                    #
    #-------------------------------------------------#

    @commands.command()
    async def playerbase(self, ctx, action=None, dcid=None, playername=None):

        userid = ctx.author.id
        await ctx.message.add_reaction("🆗")
            
        if action == "set":
            #await ctx.message.add_reaction("1️⃣")
            if dcid == userid or userid in OPERATORS:
                #await ctx.message.add_reaction("2️⃣")
                if playername is not None:
                    #await ctx.message.add_reaction("3️⃣")
                    try:
                        playerbaseSet(dcid=dcid, playername=playername)
                        await ctx.message.add_reaction("✅")
                    except Exception:
                        raise commands.BadArgument("playerbase set fehlgeschlagen")
                    
                else:
                    raise commands.MissingRequiredArgument(param=commands.Parameter(name='playername', annotation=str, kind=3))
                
            else:
                await ctx.message.add_reaction("⚠️")
                #raise commands.PermissionError
            
        elif action == "remove":
            if dcid == userid or userid in OPERATORS:
                try:
                    playerbaseRemove(dcid=dcid)
                    await ctx.message.add_reaction("✅")
                except Exception:
                    raise commands.BadArgument("playerbase remove fehlgeschlagen")
            else:
                await ctx.message.add_reaction("⚠️")
                #raise commands.PermissionError
            
        elif action == "list":
            ...
            
        elif action == None:
            await ctx.message.add_reaction("⚠️")
            raise commands.MissingRequiredArgument(param=commands.Parameter(name='action', annotation=str, kind=3))
            
        else:
            raise commands.BadArgument
		
