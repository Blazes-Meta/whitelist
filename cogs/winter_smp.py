import discord
from discord.ext import commands

TARGET_CHANNEL: int = 1422662969233248327
FAKE_MESSAGE: int = 1422959270512693392
DEBUG_CHANNEL: int = 955055841772470272

class WinterSMP(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        member = payload.member
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        print(f"Winter SMP: {member.name} issued verification")

        if member.bot:
            return
        
        if payload.channel_id != TARGET_CHANNEL:
            return 
        
        if str(payload.emoji) == "🔥":
            role = self.bot.get_guild(payload.guild_id).get_role(1329087875215527977)
            await member.add_roles(role)
            await self.bot.get_channel(DEBUG_CHANNEL).send(f"{member.mention} hat mit 🔥 reagiert!")
        else:
            try:
                await member.send(f"Wir vermuten, dass du das Briefing nicht gelesen hast. Bitte lies es nochmal. Falls du es tatsächlich schon gelesen hast, ignoriere diese Nachricht.")
            except discord.Forbidden:
                await self.bot.get_channel(DEBUG_CHANNEL).send(f"{member.mention} konnte ich leider keine DM schicken.")

        if not (payload.emoji.id == 1137799137497206854 and message.id == FAKE_MESSAGE):
            await message.remove_reaction(payload.emoji, member)



async def setup(bot):
    await bot.add_cog(WinterSMP(bot))
