import asyncio

import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
GUILD = discord.Object(id=int(os.getenv("SERVER_ID_TEST_SERVER")))

# Initizialize intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot Command prefix
bot = commands.Bot(command_prefix=None, intents=intents)

# Sync bot commands
@bot.event
async def setup_hook():
    # await bot.load_extension("cogs.general")
    # await bot.load_extension("cogs.welcome")
    # await bot.load_extension("cogs.menu")
    await bot.tree.sync(guild=GUILD)
    print(f"Synced commands to server {GUILD.id}")

async def main():
    async with bot:
        # Load cogs
        bot.setup_hook = setup_hook
        await bot.start(BOT_TOKEN)    

#Run the bot
asyncio.run(main())





