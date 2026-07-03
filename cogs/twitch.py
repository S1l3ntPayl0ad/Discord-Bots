import os
import aiohttp
import discord

from discord.ext import tasks


class TwitchNotifier:

    def __init__(self, bot):

        self.bot = bot

        self.client_id = os.getenv("TWITCH_CLIENT_ID")
        self.client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        self.username = os.getenv("TWITCH_USERNAME")
        self.channel_id = int(os.getenv("WELCOME_token"))

        self.access_token = None
        self.live = False

        self.session = aiohttp.ClientSession()

        self.check_stream.start()

    ############################################################

    async def get_access_token(self):

        url = "https://id.twitch.tv/oauth2/token"

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        async with self.session.post(url, params=params) as response:

            if response.status == 200:

                data = await response.json()

                self.access_token = data["access_token"]

                return True

            print("Unable to authenticate with Twitch.")
            return False

    ############################################################

    async def get_stream(self):

        if self.access_token is None:

            if not await self.get_access_token():
                return None

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }

        async with self.session.get(
            "https://api.twitch.tv/helix/streams",
            headers=headers,
            params={
                "user_login": self.username
            }
        ) as response:

            if response.status == 401:

                await self.get_access_token()

                return await self.get_stream()

            if response.status != 200:
                return None

            data = await response.json()

            if len(data["data"]) == 0:
                return None

            return data["data"][0]

    ############################################################

    @tasks.loop(minutes=1)
    async def check_stream(self):

        stream = await self.get_stream()

        if stream is None:

            if self.live:
                print("Stream Ended.")

            self.live = False
            return

        if self.live:
            return

        self.live = True

        channel = self.bot.get_channel(self.channel_id)

        if channel is None:
            print("Announcement channel not found.")
            return

        thumbnail = (
            stream["thumbnail_url"]
            .replace("{width}", "1280")
            .replace("{height}", "720")
        )

        embed = discord.Embed(
            title=f"🔴 {self.username} is LIVE!",
            description=stream["title"],
            color=discord.Color.green(),
            url=f"https://twitch.tv/{self.username}"
        )

        embed.add_field(
            name="🎮 Category",
            value=stream["game_name"],
            inline=True
        )

        embed.set_image(url=thumbnail)

        embed.set_footer(text="Come hang out!")

        await channel.send(
            content="@everyone\nLinkXGaming is LIVE on Twitch! Click the link below to join and enjoy the shenanigans!",
            embed=embed
        )

        print("Announcement sent!")

    ############################################################

    @check_stream.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    ############################################################

    async def close(self):
        await self.session.close()