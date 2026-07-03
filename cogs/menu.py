import discord
import os
from discord.ext import commands
from .views import MenuView


MENU_CHANNEL_ID = int(os.getenv("WELCOME_token", 0))


class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(MENU_CHANNEL_ID)
        if channel is None:
            print("Menu channel not found.")
            return

        async for message in channel.history(limit=50):
            if (
                message.author == self.bot.user
                and "<!-- MENU_SYSTEM -->" in message.content
            ):
                await message.delete()

        await channel.send(
            """<!-- MENU_SYSTEM -->

# Menu System
Choose an item from one of the dropdowns below.
""",
            view=MenuView()
        )
        print("Menu created.")


async def setup(bot):
    await bot.add_cog(Menu(bot))