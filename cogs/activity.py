import discord
from discord.ext import commands, tasks
from itertools import cycle

class Activity(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot_statuses = cycle(["Minecraft", "Minecraft"])  # Liste aller Bot-Status
        self.change_status.start()  # Startet den Bot-Status-Loop, wenn der Cog geladen wird

    @tasks.loop(seconds=5)
    async def change_status(self):
        # Ändert den Bot-Status
        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(next(self.bot_statuses)))

    @change_status.before_loop
    async def before_change_status(self):
        # Warte darauf, dass der Bot bereit ist, bevor der Loop startet
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COGS] {__name__} is ready")

async def setup(bot):
    await bot.add_cog(Activity(bot))