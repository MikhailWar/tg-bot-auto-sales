
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from data.config import admins
from filters import IsNotRefferal
from keyboards.inline import show_item_function
from loader import dp, db, bot


class InlineState(StatesGroup):
    inline_mode = State()


@dp.inline_handler(IsNotRefferal())
async def conclusion_buttons(query: types.InlineQuery):
    await db.add_user(user_id=query.from_user.id, full_name=query.from_user.full_name)
    await query.answer(
            results=[],
            switch_pm_text="Бот недоступен. Подключить бота",
            switch_pm_parameter=admins[0],
            cache_time=5)

@dp.inline_handler(text="")
async def conclusion_items(query: types.InlineQuery, state: FSMContext):
    await InlineState.inline_mode.set()
    bot_username = (await bot.get_me()).username
    media = []
    items_database = [tuple(item) for item in await db.select_items_all()]
    names = [name[1] for name in items_database]
 
    # сортировка по алфавиту
    items_database_in_the_alphabet = []
    for name in sorted(names):
        item = [tuple(item) for item in await db.select_name_items(name)]
        items_database_in_the_alphabet.append(*item)

    for item_id, name, description, price, price_btc, photo, currency, count in items_database_in_the_alphabet:

        media.append(types.InlineQueryResultArticle(id=f"{item_id}",
                                                    title=f"{name}",
                                                    input_message_content=types.InputMessageContent(
                                                        message_text=f"<b>{name}</b>\n"
                                                                     f"Описание товара:"
                                                                     f"{description}\n"
                                                                     f"Количество товара: {count}",
                                                        parse_mode="HTML"
                                                    ),
                                                    thumb_url=photo,
                                                    description=f"Цена товара: {price_btc} BTC",
                                                    reply_markup=show_item_function(item_id, bot_username)

                                                    ))
    await query.answer(results=media, cache_time=3)
    await state.finish()

@dp.inline_handler(regexp=r"[A-Za-zА-Яа-я]")
async def conclusion_select_item(query: types.InlineQuery, state: FSMContext):
    bot_username = (await bot.get_me()).username
    await InlineState.inline_mode.set()
    media = []
    items_database = [tuple(item) for item in await db.select_items(name=query.query)]

    for item_id, name, description, price, price_btc, photo, currency, count in items_database:

        media.append(types.InlineQueryResultArticle(id=f"{item_id}",
                                                    title=f"{name}",
                                                    input_message_content=types.InputMessageContent(
                                                        message_text=f"<b>{name}</b>\n"
                                                                     f"Описание товара: "
                                                                     f"{description}\n"
                                                                     f"Количество товара: {count}",
                                                        parse_mode="HTML"
                                                    ),
                                                    thumb_url=photo,
                                                    description=f"Цена товара: {price_btc} BTC",
                                                    reply_markup=show_item_function(item_id, bot_username)

                                                    ))

    await query.answer(results=media)
    await state.finish()
