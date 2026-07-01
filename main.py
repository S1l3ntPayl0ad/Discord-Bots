import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")
GUILD = discord.Object(id=int(os.getenv("SERVER_ID")))

# Initizialize intents
intents = discord.Intents.default()
intents.message_content = True

# Bot Command prefix
bot = commands.Bot(command_prefix="/", intents=intents)

# Sync bot commands
@bot.event
async def setup_hook():
    await bot.tree.sync(guild=GUILD)
    print(f"Synced commands to server {GUILD.id}")

# Bot command to say hello back to the user
@bot.tree.command(
    name="hello",
    description="Says hello to the user"
)
async def hello(
    interaction: discord.Interaction
):
    await interaction.response.send_message(
        f"Hello {interaction.user.mention}!"
    )

# Bot command to tell user to touch grass
@bot.tree.command(
        name="grass",
        description="Tell someone to touch grass"
)
@app_commands.describe(
    member="Who to tell to touch grass"
)
async def grass(
    interaction: discord.Interaction,
    member: discord.Member
):
    await interaction.response.send_message(
        f"{member.mention}, {interaction.user} wants you to go touch some grass!"
    )


#Run the bot
bot.run(BOT_TOKEN)





