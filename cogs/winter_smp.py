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
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        print("Notice")
        member = payload.member
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)


        if member.bot:
            return
        
        if payload.channel_id != TARGET_CHANNEL:
            return 
        
        if message.id == TARGET_MESSAGE:
            if str(payload.emoji) == "🔥":
                await self.bot.get_channel(DEBUG_CHANNEL).send(f"{member.mention} hat mit 🔥 reagiert!")
            await message.remove_reaction(payload.emoji, member)
        elif message.id == FAKE_MESSAGE:   
            try:
                await member.send(f"Wir vermuten, dass du das Briefing nicht gelesen hast. Bitte lies es nochmal. Falls du es tatsächlich schon gelesen hast, ignoriere diese Nachricht.")
            except discord.Forbidden:
                await self.bot.get_channel(DEBUG_CHANNEL).send(f"{member.mention} konnte ich leider keine DM schicken.")
            if payload.emoji.id != 1137799137497206854:
                await message.remove_reaction(payload.emoji, member)
        else:
            await message.remove_reaction(payload.emoji, member)

async def setup(bot):
    await bot.add_cog(WinterSMP(bot))
