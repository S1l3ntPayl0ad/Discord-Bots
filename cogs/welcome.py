import os 
import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)

        if channel:
            await channel.send(
                f"Welcome to the Squad {member.mention}! Don't forget to introduce yourself in <#Channel ID>. Make sure to read the rules in <#Channel ID>. Don't forget to check out the other channels and have fun! >"
            )

    async def setup(bot):
        await bot.add_cog(Welcome(bot))