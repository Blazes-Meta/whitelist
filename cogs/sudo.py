import discord
from discord.ext import commands
from acemeta import log


class Bot_Sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log(f"[COGS] {__name__} is ready")
        
    #-------------------------------------------------#
    #                  Sudo-Befehle                   #
    #-------------------------------------------------#

    @commands.command()
    async def sudo(self, ctx, arg1=None, arg2=None):
        log(f"[SUDO] {ctx.author.name} ({ctx.author.id}) executed \"{ctx.message.content}\" in {ctx.guild.name} ({ctx.guild.id})")
        
        #-------------------------------------------------#
        #                      Sync                       #
        #-------------------------------------------------#
        if arg1 == "sync":
            if arg2 == str(self.bot.user.id):
                await self.bot.tree.sync()

                await ctx.message.add_reaction("✅")
                embed = discord.Embed(description=f"Es wurde eine Anfrage zur Synchronisation der App-Commands für alle Guilden versendet.\nDie Synchronisation kann einige Minuten bis Stunden dauern.", color=3908961)
                embed.set_author(name="Synchronisations-Anfrage versendet", icon_url="https://cdn.discordapp.com/emojis/1233093791657758740.webp")
                await ctx.reply(embed = embed, mention_author=False, silent=True, delete_after=10)
                
                log(f"[SYNC] Global synchronization of all App-Commands requested. Synchronization can take several minutes to hours.")
            
            elif arg2 == None:
                raise commands.MissingRequiredArgument(param=commands.Parameter(name='arg2', annotation=str, kind=3))
            else:
                raise commands.BadArgument("Falscher Code")
        
        #-------------------------------------------------#
        #                  Error-Raiser                   #
        #-------------------------------------------------#
        elif arg1 == None:
            raise commands.MissingRequiredArgument(param=commands.Parameter(name='arg1', annotation=str, kind=3))
        else:
            raise commands.MissingRequiredArgument(param=commands.Parameter(name='arg1', annotation=str, kind=3))
        
async def setup(bot):
    await bot.add_cog(Bot_Sudo(bot))