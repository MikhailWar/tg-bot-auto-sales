import logging
import random
from decimal import getcontext, Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from data.currency import currency
from filters import IsAdmin
from keyboards.inline import accept_btn, random_id, currency_function, accept_to_add_item, \
    generation_random_call_inline_mode
from loader import dp, db, bot, con_currency
from states import AddItem
from utils.misc import parse_amount
from utils.misc.amount import ErrorFormat


@dp.message_handler(Command("item_add"), IsAdmin())
async def add_admin_bot(message: types.Message):
    await message.answer(text="Здравствуйте, вы хотите добавить новый товар в нашу базу?", reply_markup=accept_btn)
    await message.delete()
    await AddItem.accept.set()

@dp.message_handler(Command("item_add"))
async def add_admin_bot(message: types.Message):
    await message.answer(text="У вас недостаточно прав к этой команде.")
    await message.delete()

@dp.callback_query_handler(lambda call: call.data == "yes", state=AddItem.accept)
async def accept_yes(call: types.CallbackQuery):
    await call.message.edit_text(text="Введите айди товара или нажимите на кнопку «сформировать рандомный айди»",
                                 reply_markup=random_id)
    await AddItem.next()


@dp.callback_query_handler(lambda call: call.data == "no", state=AddItem.accept)
async def accept_no(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.edit_text(text="Вы отменили добавление товара. Хорошего вам дня!")
    await state.finish()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer("Вы отменили добавления товара! Всего хорошего.", reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text="random_id", state=AddItem.id_item)
async def random_id_item(call: types.CallbackQuery, state: FSMContext):
    item_id = random.randint(1, 1000000)
    message = await call.message.edit_reply_markup()
    await message.edit_text(f"Ваш ID товара: {item_id}.\n"
                            f"Напишите название товара")

    await state.update_data(id_item=item_id)
    await AddItem.next()


@dp.message_handler(state=AddItem.name)
async def write_name_item(message: types.Message, state: FSMContext):
    _name_item = message.text[1:]
    first_letter = message.text[:1].upper()
    name_item = first_letter+_name_item
    print(name_item)
    await state.update_data(name=name_item)
    await message.answer("Введите описание товара")
    await AddItem.next()


@dp.message_handler(state=AddItem.description)
async def write_description_item(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Какая цена вашего товара?")
    await AddItem.next()

# РАБОТА С ДЕНЬГАМИ
@dp.message_handler(regexp=r"[\d+\s.\d.\d+]", state=AddItem.price)
async def setting_price_item(message: types.Message, state: FSMContext):
    #  100 000 или 100000
    try:
        price_str = parse_amount(message.text)

        getcontext().prec=2
        price = Decimal(f"{price_str}")
        await state.update_data(price=price)
        await message.answer("Отправьте ссылку на фото товара")
        await AddItem.next()

    except:
        await message.answer("Неправильный формат")
        return


@dp.message_handler(regexp=r"(?P<url>https?://[^\s]+)", state=AddItem.photo)
async def setting_photo_item_url(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await message.answer("Выбирете валюту в которой товар планируете продавать",
                         reply_markup=currency_function(currency))
    await AddItem.next()


@dp.callback_query_handler(text=[index for name, index in currency], state=AddItem.currency)
async def setting_currency_item(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await state.update_data(currency=call.data)

    # переводим в биткойны
    price_btc = await con_currency.convert_currency(
        from_currency=call.data,
        to_currency="BTC",
        count=data.get('price'),
        multiply=True
    )

    # обноваляем цены в состояние
    await state.update_data(price_btc=price_btc)
    await call.message.edit_reply_markup()
    await call.message.edit_text(text="Введите количество товаров.")

    await AddItem.next()


@dp.message_handler(regexp=r"[\d+\s.\d.\d+]", state=AddItem.count)
async def setting_count_item(message: types.Message, state: FSMContext):
    bot_username = (await bot.get_me()).username
    try:
        count = parse_amount(message.text)
    except ErrorFormat:
        await message.answer("Вы ввели неправильный формат")
        return
    # обновляем count
    await state.update_data(count=int(count))

    # достаем значения
    data = await state.get_data()  # получаем данные в виде словаря
    price = data.get('price')
    price_btc = data.get('price_btc')
    item_id = data.get('item_id')
    currency_item = data.get('currency')

    text = [

        f"<b>{data.get('name')}</b>",  # название товара
        f"{data.get('description')}",
        f"Количество товара:<b>{data.get('count')}</b>",
        f"Цена товара: {price:.2f} {currency_item} конвертация в BTC <code>{price_btc}</code>"
    ]

    await message.delete()
    await message.answer_photo(
        photo=data.get('photo'),
        caption="\n".join(text),
        reply_markup=accept_to_add_item()
    )
    await AddItem.end_accept.set()


@dp.callback_query_handler(text="yes_add", state=AddItem.end_accept)
async def add_item_to_database(call: types.CallbackQuery, state: FSMContext):
    bot_username = (await bot.get_me()).username
    data = await state.get_data()  # получаем данные в виде словаря
    data_values = data.values()  # достаем данные из словаря

    await db.add_item_base(tuple(data_values))  # добавляем в базу данных

    await call.message.delete()
    await call.message.answer(text="Вы добавили товар в базу данных.\n"
                                   f"Для просмотра перейдите - впишите в строку @{bot_username}",
                              reply_markup=generation_random_call_inline_mode("Айфон"))
    await state.finish()


@dp.message_handler(text="no_add", state=AddItem.end_accept)
async def no_add_item(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="Вы отменили добавление товара")
    await state.finish()
