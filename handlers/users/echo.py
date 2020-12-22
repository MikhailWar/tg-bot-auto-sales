from aiogram import types

from data.config import files_id
from loader import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(f"Включен эхо режим: {message.text}" )
