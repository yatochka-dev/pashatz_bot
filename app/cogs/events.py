import os

import disnake
from disnake.ext.commands import Cog

from app import Bot
from app.services.PashatzService import PashatzService


class Events(Cog, PashatzService):
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def get_channel(guild: disnake.Guild):
        for channel in guild.channels:
            if isinstance(channel, disnake.TextChannel):
                can_send = channel.permissions_for(guild.me).send_messages
                if can_send:
                    return channel
                else:
                    continue

    @Cog.listener(
        "on_ready",
    )
    async def is_ready(self):
        self.bot.logger.info(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        self.bot.logger.info(f"Started bot in {os.getenv('STATE_NAME').title()} mode.")
        self.bot.logger.info("------")

    @Cog.listener(
        "on_member_join"
    )
    async def on_member_join(self, member: disnake.Member):
        await self.process(member, self.bot)


def setup(bot: Bot):
    bot.add_cog(Events(bot))
