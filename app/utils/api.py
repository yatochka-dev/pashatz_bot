import asyncio

import disnake
from starlette.requests import Request

from app import Bot
from app.loggs import logger


def get_bot_from_request(request: Request) -> Bot:
    bot: Bot = request.app.state.bot

    if not bot.is_ready():
        asyncio.run(bot.wait_until_ready())

    return bot


async def safely_add_role(member: disnake.Member, role: int):
    try:
        await member.add_roles(member.guild.get_role(role))
    except Exception as ex:
        logger.debug(f"Failed to add role {role} to {member}, \n {ex}")
