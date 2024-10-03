import os
import asyncio
import discord
from discord.ext import commands, tasks
from discord.utils import setup_logging
from dotenv import load_dotenv
from acemeta import log

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def loadCogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            log(f"[COGS] cogs/{filename} is loaded")

async def main():
    load_dotenv() # Läd die Umgebungsvariabeln
    async with bot:
        await loadCogs()
        setup_logging()
        await bot.start(str(os.getenv("BOT_TOKEN")))

@bot.event
async def on_ready():
    log(f"[AUTH] Bot is connected")
    log(f"[AUTH] Logged in as {bot.user} (ID: {bot.user.id})")

asyncio.run(main()) # Diese Zeile wird fortlaufend ausgeführt und sollte deswegen am Ende stehen
