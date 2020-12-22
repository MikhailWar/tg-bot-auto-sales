from aiogram import types

from data.config import admins
from filters import IsNotRefferal

from loader import dp, bot, db


@dp.message_handler(IsNotRefferal(), content_types=types.ContentType.ANY)
async def message_users_not_from_referral(message: types.Message):
    bot_username = (await bot.get_me()).username
    link_refferal = f"https://t.me/{bot_username}?start={admins[0]}"
    await message.answer("Чтобы использовать этого бота введите код приглашения, либо пройдите по реферальной ссылке\n"
                         f"Для вас сгенерирована ссылка: <a href='{link_refferal}'>Кликни</a>")