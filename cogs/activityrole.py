import discord
from discord import app_commands
from discord.ext import commands, tasks
from mcstatus import JavaServer
from lib.dbinterface import *

guild_id = 890190896530849792
role_id = 1329087875215527977

PLAYERBASE_LOCAL = "tmp/playerbase.db"
pb = Playerbase(dbpath=PLAYERBASE_LOCAL)
playerbase = pb.listEntries()

async def setup(bot):
    await bot.add_cog(ActivityRole(bot))

class ActivityRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(minutes=1)
    async def assign_role_loop(self):
        server_address = "LvLSmpS2.aternos.me"
        server_port = 25565

        try:
            server = JavaServer.lookup(f"{server_address}:{server_port}")
            query = server.query()
            players = query.players.names

            user_ids = []

            if players:
                for player in players:
                    for key, value in playerbase.items():
                        if value == player:
                            user_ids.append(key)

        except Exception as e:
            print(e)

        guild: discord.Guild = self.bot.get_guild(self.guild_id)
        if not guild:
            print("Guild nicht gefunden.")
            return

        role = guild.get_role(self.role_id)
        if not role:
            print("Rolle nicht gefunden.")
            return

        for user_id in guild.members:
            member = guild.get_member(user_id)
            if member and role not in member.roles:
                try:
                    await member.add_roles(role)
                    print(f"Rolle '{role.name}' zu {member.name} hinzugefügt.")
                except discord.Forbidden:
                    print(f"Keine Berechtigung, um {member.name} die Rolle hinzuzufügen.")
                except discord.HTTPException as e:
                    print(f"Fehler beim Hinzufügen der Rolle: {e}")

            else:
                try:
                    await member.remove_roles(role)
                    print(f"Rolle '{role.name}' von {member.name} entfernt.")
                except discord.Forbidden:
                    print(f"Keine Berechtigung, um von {member.name} die Rolle zu entfernen.")
                except discord.HTTPException as e:
                    print(f"Fehler beim Entfernen der Rolle: {e}")


    @assign_role_loop.before_loop
    async def before_assign_role_loop(self):
        print("Warte, bis der Bot bereit ist...")
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.assign_role_loop.cancel()