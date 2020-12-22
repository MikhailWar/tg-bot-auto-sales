from aiogram import types

accept_btn = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="Да, хочу добавить товар.", callback_data="yes"),
        types.InlineKeyboardButton(text="Нет, не хочу.", callback_data="no")

    ]
])