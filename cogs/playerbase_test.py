OPERATORS = []#.append(720992368110862407)
DATABASE = 'playerbase.db'

import sqlite3
import discord
from discord.ext import commands
from lib.dbinterface import *

async def setup(bot):
    await bot.add_cog(PlayerbaseTest(bot))

class PlayerbaseTest(commands.Cog):
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
        #await ctx.message.add_reaction("🆗")
            
        if action == "set":
            #await ctx.message.add_reaction("1️⃣")
            try:
                dcid = int(dcid)
            except:
                raise commands.BadArgument("Die Discord-ID ist ungültig")
            
            if dcid == userid or userid in OPERATORS:
                #await ctx.message.add_reaction("2️⃣")
                if playername is not None:
                    #await ctx.message.add_reaction("3️⃣")
                        playerbaseSet(dcid=dcid, playername=playername)
                        await ctx.message.add_reaction("✅")
                        await ctx.reply(f"<@{dcid}> wurde mit {playername} verbunden", mention_author=False)
                    
                else:
                    raise commands.MissingRequiredArgument(param=commands.Parameter(name='playername', annotation=str, kind=3))
                
            else:
                await ctx.message.add_reaction("⚠️")
                #raise commands.PermissionError
            
        elif action == "remove":
            try:
                dcid = int(dcid)
            except:
                raise commands.BadArgument("Die Discord-ID ist ungültig")
            
            if dcid == userid or userid in OPERATORS:
                try:
                    playerbaseRemove(dcid=dcid)
                    await ctx.message.add_reaction("✅")
                    await ctx.reply(f"<@{dcid}> ist nichtmehr mit einem Minecraft-Account verbunden", mention_author=False)

                except NoEntryError:
                    raise commands.BadArgument(f"Es ist kein Spieler auf <@{dcid}> registriert")
                
            else:
                await ctx.message.add_reaction("⚠️")
                raise commands.MissingPermissions(message="Dir fehlen Berechtigungen")
            
        elif action == "list":
            ...
            
        elif action == None:
            #await ctx.message.add_reaction("⚠️")
            raise commands.MissingRequiredArgument(param=commands.Parameter(name='action', annotation=str, kind=3))
            
        else:
            raise commands.BadArgument("Das Argument muss eines von `set`, `remove` und `list` sein")
		
