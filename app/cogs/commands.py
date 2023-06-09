from disnake.ext.commands import Cog, slash_command

from app import Bot, md
from app.decorators import db_required
from app.embedding import Embed
from app.services.PashatzService import PashatzService
from app.types import CommandInteraction


class Command(Cog, PashatzService):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    @db_required
    async def ping(self, inter: CommandInteraction) -> None:
        print("Ping command")
        current_latency = round(self.bot.latency * 1000, 2)

        match current_latency:
            case x if x <= 50:
                color = (0, 255, 0)

            case x if x <= 100:
                color = (255, 255, 0)

            case x if x <= 150:
                color = (255, 165, 0)

            case x if x <= 200:
                color = (255, 0, 0)

            case _:
                color = (0, 0, 0)

        await inter.send(
            embed=Embed(
                title="Pong!",
                description=f"{md('Latency'):bold}:{current_latency}ms",
                user=inter.user,
            ).as_color(color)
        )


def setup(bot: Bot):
    bot.add_cog(Command(bot))
