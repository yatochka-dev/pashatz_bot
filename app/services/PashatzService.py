import disnake

from app import Bot
from app.services.index import AppService
from app.views import PashatzMahlakot

pashatzRole = 1091305673150713898


class PashatzService(AppService):
    async def process(self, member: disnake.Member, bot: Bot):
        await member.add_roles(member.guild.get_role(pashatzRole))
        await member.send(
            content="Choose your mahlaka!",
            view=PashatzMahlakot(self.bot, member)
        )

