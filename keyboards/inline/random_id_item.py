from aiogram import types

random_id = types.InlineKeyboardMarkup(
    inline_keyboard=[[
        types.InlineKeyboardButton(text="Рандомный ID товара", callback_data="random_id")
    ]
    ]
)