from aiogram import types

from keyboards.inline.CallBackData import buy_callback_factory


def buy_item_func_start(item_id: int,
                        price: str, ):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Купить", callback_data=buy_callback_factory.new(item_id=item_id,
                                                                                                 price=price))
            ]
        ]
    )
    return keyboard


def buy_item_func_end(pressed_discount: bool = False):
    markup = types.InlineKeyboardMarkup(row_width=2)

    keyboard = (("Оплатил", "paid"),
                ("Применить скидку", "discount"),
                ("Отменить покупку", "cancel"))
    if pressed_discount:
        keyboard = (("Оплатил", "paid"),
                    ("Отменить покупку", "cancel"))

    for text, data in keyboard:
        markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))

    return markup

def show_item_function(item_id: int, bot_username):
    show_item = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Показать товар",
                                    url=f"https://t.me/{bot_username}?start={item_id}")
         ]
    ])

    return show_item
