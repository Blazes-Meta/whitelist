import discord
from discord.ext import commands

TARGET_CHANNEL: int = 1422662969233248327
TARGET_MESSAGE: int = 1422959267102851212
FAKE_MESSAGE: int = 1422959270512693392
DEBUG_CHANNEL: int = 1424326556771418112

class WinterSMP(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        
        if reaction.message.channel.id != TARGET_CHANNEL:
            return 
        
        if reaction.message.id == TARGET_MESSAGE:
            if str(reaction.emoji) == "🔥":
                await self.bot.get_channel(DEBUG_CHANNEL).send(f"{user.mention} hat mit 🔥 reagiert!")
            await reaction.remove(user)
        elif reaction.message.id == FAKE_MESSAGE:   
            try:
                await user.send(f"Wir vermuten, dass du das Briefing nicht gelesen hast. Bitte lies es nochmal. Falls du es tatsächlich schon gelesen hast, ignoriere diese Nachricht.")
            except discord.Forbidden:
                await self.bot.get_channel(DEBUG_CHANNEL).send(f"{user.mention} konnte ich leider keine DM schicken.")
            if reaction.emoji.id != 1137799137497206854:
                await reaction.remove(user)
        else:
            await reaction.remove(user)

async def setup(bot):
    await bot.add_cog(WinterSMP(bot))
