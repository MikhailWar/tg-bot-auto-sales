import re

from aiogram import types


def currency_function(parameters: tuple):
    currency_btn = types.InlineKeyboardMarkup(row_width=2)
    for name, index in parameters:
        currency_btn.insert(types.InlineKeyboardButton(text=f"{name}", callback_data=f"{index}"))

    return currency_btn
