from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config


class AdminMessageFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (str(obj.chat.id) == config.misc.admin_group) == self.is_admin


class AdminCallbackQueryFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: CallbackQuery, config: Config) -> bool:
        return (str(obj.message.chat.id) == config.misc.admin_group) == self.is_admin
