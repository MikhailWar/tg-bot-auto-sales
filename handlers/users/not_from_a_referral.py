from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from data.config import admins
from filters import IsNotRefferal

from loader import dp, bot


@dp.message_handler(IsNotRefferal(), content_types=types.ContentType.ANY)
async def message_users_not_from_referral(message: types.Message):
    link_refferal = await get_start_link(admins[0])
    await message.answer("Чтобы использовать этого бота введите код приглашения, либо пройдите по реферальной ссылке\n"
                         f"Для вас сгенерирована ссылка: <a href='{link_refferal}'>Кликни</a>")