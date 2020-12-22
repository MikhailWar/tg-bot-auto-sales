from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in admins

