from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class IsNotRefferal(BoundFilter):

    def __init__(self, *user_id):
        if not user_id:
            self.user_id = None
        self.user_id = list(*user_id)

    # Проверка на реферала
    async def check(self, message: types.Message) -> bool:
        await db.add_user(user_id=message.from_user.id, full_name=message.from_user.full_name)
        user_id_from_referral = await db.select_id_refer_user(user_id=message.from_user.id)

        if not user_id_from_referral:
            return True
