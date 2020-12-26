from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline import generation_random_call_inline_mode
from loader import dp, db

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await db.add_user(user_id=message.from_user.id, full_name=message.from_user.full_name)
<<<<<<< HEAD
    await message.answer(f'Привет, {message.from_user.full_name}!',
                         reply_markup=generation_random_call_inline_mode(""))
=======
    await message.answer(f'Привет, {message.from_user.full_name}!')
>>>>>>> 3f0ca18ca501d02473a764cc027e65da60dcbf26

