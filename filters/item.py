from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class CheckItems(BoundFilter):

    async def check(self, message: types.bot_command) -> bool:
        try:
            items_id = [item_id[0] for item_id in [tuple(item_id) for item_id in await db.select_id_items_all()]]
            item_id = message.get_args()

            if int(item_id) in items_id:
                return True
        except:
            pass
