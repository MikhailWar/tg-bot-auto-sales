from aiogram import types

from loader import bot


def accept_to_add_item(bot_username:  str, item_id: int):
    # цена
    # принять отказать в добавлении

    yes_no = (
        ("Принять товар. Добавить в базу.", "yes_add"),
        ("Отменить добавления товара.", "no_add")
    )

    keyboard_add = types.InlineKeyboardMarkup(row_width=2)
    keyboard_add.add(types.InlineKeyboardButton(text="Показать товар", url=f"https://t.me/{bot_username}?start={item_id}"))
    buttons = []
    for name, data in yes_no:
        buttons.append(types.InlineKeyboardButton(text=f"{name}", callback_data=f"{data}"))

    keyboard_add.row(*buttons)

    return keyboard_add

