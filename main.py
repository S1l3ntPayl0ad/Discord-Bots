import asyncio

import discord
import os
from cogs.twitch import TwitchNotifier
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
async def setup_hook():
    # await bot.load_extension("cogs.general")
    # await bot.load_extension("cogs.welcome")
    # await bot.load_extension("cogs.menu")
    bot.twitch = TwitchNotifier(bot)

    await bot.tree.sync(guild=GUILD)
    print(f"Synced commands to server {GUILD.id}")

async def main():
    async with bot:
        bot.setup_hook = setup_hook

        try:
            await bot.start(BOT_TOKEN)

        finally:
            if hasattr(bot, "twitch"):
                await bot.twitch.close()   

#Run the bot
asyncio.run(main())





