from typing import Callable

import disnake
from disnake import MessageInteraction
from disnake.ui import Item, View

from app import Bot, Embed, safely_add_role
from app.exceptions import BotException
from app.types import DiscordUtilizer


class BaseView(View):
    def __init__(self, bot: Bot, user: DiscordUtilizer, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.bot = bot

    async def interaction_check(self, interaction: MessageInteraction):
        """

        Exception codes:
            1 - Forbidden
            2 - Not found
        """
        BotException.assert_value(
            not interaction.user.bot, error_code=403, message="This interaction can be used by bots"
        )

        BotException.assert_value(
            interaction.user.id == self.user.id,
            error_code=403,
            message="You can't use this interaction",
        )
        return True

    async def on_error(self, error: Exception, item: Item, interaction: MessageInteraction) -> None:
        if isinstance(error, BotException):

            await interaction.send(embed=error.to_embed(user=interaction.user), ephemeral=True)
        else:
            await interaction.response.send_message("An unknown error occured.", ephemeral=True)
            raise error


class PaginationView(BaseView):
    def __init__(
        self,
        bot: Bot,
        user: DiscordUtilizer,
        pages: list[Embed],
        **kwargs,
    ):
        super().__init__(bot, user, **kwargs)
        self.pages = pages
        self.current_page = 0

        self._update_state()

    def _update_state(self) -> None:
        if len(self.pages) == 1:
            self.clear_items()
            self.stop()

        self.first_page.disabled = self.prev_page.disabled = self.current_page == 0
        self.last_page.disabled = self.next_page.disabled = self.current_page == len(self.pages) - 1

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.blurple)
    async def first_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page = 0
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.secondary)
    async def prev_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.red, custom_id="delete")
    async def remove(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(view=None)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
    async def next_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page += 1
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.blurple)
    async def last_page(self, _button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.current_page = len(self.pages) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.pages[self.current_page], view=self)


class MahlakaButton(disnake.ui.Button):
    def __init__(self, mahlaka_num: int, handle_click: Callable, bot: Bot, /):
        super().__init__(label=f" {mahlaka_num} מחלקה", style=disnake.ButtonStyle.secondary)
        self.mahlaka_num: int = mahlaka_num
        self.handle_click = handle_click
        self.server = 1091302701448581172
        self.bot = bot
        self.mahlakot = {
            1: 1091307602857693204,
            2: 1091307779916058776,
            3: 1091307945901436958,
            4: 1091308001987661844,
            5: 1091308040579465276,
            6: 1091308072217088101,
            7: 1091308095034105956,
            8: 1091308120715825183,
            9: 1091308154471583794,
            10: 1091308186042114068,
            11: 1091308219550408814,
        }

    async def callback(self, interaction: MessageInteraction, /):
        await self.add_mahlaka(self.mahlaka_num, interaction)
        await self.handle_click(interaction)
        await interaction.user.send(
            "המחלקה נוספה בהצלחה! תודה על ההשתתפות!",
        )

    async def add_mahlaka(self, mahlaka_num: int, inter: MessageInteraction) -> None:
        guild = self.bot.get_guild(self.server)
        await safely_add_role(guild.get_member(inter.author.id), self.mahlakot[mahlaka_num])


class PashatzMahlakot(BaseView):
    def __init__(self, bot: Bot, user: DiscordUtilizer, **kwargs):
        super().__init__(bot, user, **kwargs)
        self._set_buttons()

    async def handle_click(self, interaction: MessageInteraction):
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)

    def _set_buttons(self) -> None:
        for i in range(1, 12):
            self.add_item(MahlakaButton(i, self.handle_click, self.bot))
