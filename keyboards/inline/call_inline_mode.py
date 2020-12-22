import random

from aiogram import types


def generation_random_call_inline_mode(text: str):

    call_inline_mode_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[

        types.KeyboardButton(text="Перейти в инлайн режим", switch_inline_query_current_chat=text)
    ]])
    return call_inline_mode_keyboard
