import os
import asyncio
import discord
from discord.ext import commands, tasks
from discord.utils import setup_logging
from dotenv import load_dotenv
from lib.github import Repository

PLAYERBASE_LOCAL = "tmp/playerbase.db"

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
repo = Repository(repository="Blazes-Meta/whitelist", token=GITHUB_TOKEN)

async def loadCogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"[COGS] cogs/{filename} is loaded")

async def main():
    load_dotenv() # Läd die Umgebungsvariabeln
    async with bot:
        await loadCogs()
        setup_logging()
        await bot.start(str(BOT_TOKEN))

@bot.event
async def on_ready():
    print(f"[AUTH] Bot is connected")
    print(f"[AUTH] Logged in as {bot.user} (ID: {bot.user.id})")
    #bot.tree.clear_commands(guild=None)

asyncio.run(main()) # Diese Zeile wird fortlaufend ausgeführt und sollte deswegen am Ende stehen
