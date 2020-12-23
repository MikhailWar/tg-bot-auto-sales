from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import my_profile
from loader import dp, db

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await db.add_user(user_id=message.from_user.id, full_name=message.from_user.full_name)
    await message.answer(f'Привет, {message.from_user.full_name}!')

