import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /hello
    @app_commands.command(name="hello", description="Says hello to the user")
    async def hello(self, interaction:discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")

    # /grass
    @app_commands.command(name="grass", description="Tell someone to touch grass")
    @app_commands.describe(member="Who to tell to touch grass")
    async def grass(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{member.mention}, {interaction.user} wants you to go touch some grass!")

    # /snow
    @app_commands.command(name="snow", description="Tell someone to touch snow")
    @app_commands.describe(member="Who to tell to touch snow")
    async def snow(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{member.mention}, {interaction.user} wants you to go touch some snow!")
        
# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(General(bot))
