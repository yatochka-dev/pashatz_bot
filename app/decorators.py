import functools

import disnake

from .types import CommandInteraction


def db_required(coro):
    @functools.wraps(coro)
    async def wrapper(self, inter: CommandInteraction, *args, **kwargs):
        pass

        await coro(self, inter, *args, **kwargs)

    return wrapper
