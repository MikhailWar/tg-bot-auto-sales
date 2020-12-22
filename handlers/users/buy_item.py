import logging
import random
from decimal import Decimal, getcontext

import blockcypher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from data import config
from data.item_id_buy import items_id
from filters import CheckItems, IsAdmin, IsNotRefferal
from keyboards.inline import buy_item_func_start, buy_item_func_end
from keyboards.inline.CallBackData import buy_callback_factory
from loader import dp, db, con_currency
from states import ItemBuy
from utils.misc import Payment, send_message_admin_successful_order
from utils.misc.bitcoin_payment import NotConfirmed, NoPaymentFound


@dp.message_handler(CheckItems(),
                    Command("start"))
async def show_item(message: types.Message):
    item_id = message.get_args()
    item_id, name, description, price, price_btc, photo, currency, count = await db.select_items_all_where_items_id(
        int(item_id))

    text = "\n".join([
        f"<b>{name}</b>",
        f"{description}",
        f"Цена товара: <code>{price_btc} BTC</code> - это {price:.2f} {currency}",
        f"Сейчас {count} на складе"

    ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=buy_item_func_start(item_id,
                                                                                           price_btc))


@dp.callback_query_handler(buy_callback_factory.filter())
async def buy_item(call: types.CallbackQuery, callback_data: dict):
    await call.answer()

    item_id = callback_data.get("item_id")

    items_id[call.from_user.id] = int(item_id)  # мы добавляем в словарь юзера с айди товара, который он выбрал

    _, currency = tuple(await db.select_name_and_currency_items(item_id=int(item_id)))
    await call.message.delete()
    await call.message.answer("Введите количество товара: ")

    await ItemBuy.count.set()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.answer("Вы отменили покупку товара. Возвращайтесь еще!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(regexp=r"\d+", state=ItemBuy.count)
async def setting_count_item(message: types.Message, state: FSMContext):
    item_id = items_id[message.from_user.id]  # достааем айди товара
    item_id, name, description, price, price_btc, photo, currency, count = await db.select_items_all_where_items_id(
        item_id)
    await state.update_data(item_id=item_id)

    if int(message.text) > count:
        await message.answer("Вы выбрали больше товара, чем есть у нас складе.\n"
                             f"Сейчас на складе: <b>{count}</b>.")
    else:
        await state.update_data(count=int(message.text))
        await message.answer("Введите адрес доставки")
        await ItemBuy.next()


@dp.message_handler(state=ItemBuy.delivery_address)
async def setting_delivery_address(message: types.Message, state: FSMContext):
    await state.update_data(delivery=message.text)
    data = await state.get_data()
    item_id = items_id[message.from_user.id]  # достааем айди товара
    del items_id[message.from_user.id]  # удалаяем
    item_id, name, description, price, price_btc, photo, currency, count = await db.select_items_all_where_items_id(
        item_id)
    await state.update_data(name_item=name)
    await state.update_data(delivery_address=message.text)
    the_commission = blockcypher.satoshis_to_btc(random.randint(1, 500))

    getcontext().prec = 12

    amount = (Decimal(f"{price_btc}") * Decimal(f"{data.get('count')}")) + Decimal(f"{the_commission}")
    await state.update_data(amount=Decimal(f"{amount}"))
    await message.answer(f"Вы выбрали товар: <b>{name}</b>\n"
                         f"Количество товара: <b>{data.get('count')}</b>\n"
                         f"Сумма к оплате: <code>{amount} BTC</code>"
                         f"Оплатите на этот биткойн кошелек: <code>{config.WALLET_BTC}</code>",
                         reply_markup=buy_item_func_end())

    payment = Payment(amount=float(f"{amount:.12f}"))
    payment.create()
    await state.update_data(payment=payment)

    await ItemBuy.next()


@dp.callback_query_handler(text="cancel", state=ItemBuy.paid)
async def cancel_paid(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.edit_text(text="Вы отменили покупку.")
    await state.finish()


@dp.callback_query_handler(text="discount", state=ItemBuy.paid)
async def to_apply_discount(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount_btc = data.get("amount")
    getcontext().prec = 12
    balance_user = tuple(await db.select_balance(user_id=call.from_user.id))
    balance_user = Decimal(f"{balance_user[0]}")  # amount
    rate_from_dollar_in_btc = await con_currency.convert_currency(
        from_currency="USD",
        to_currency="BTC",
        count=balance_user,
        multiply=True
    )
    amount = Decimal(f"{amount_btc}") - Decimal(f"{rate_from_dollar_in_btc}")

    if float(amount) < 0:
        await call.answer(text="Вы не можете применить скидку. Она первышает общую стоимость покупки.", show_alert=True)
        await call.message.edit_reply_markup(reply_markup=buy_item_func_end(True))
        return
    #  обновляем баланс юзера
    await db.set_balance_user(user_id=call.from_user.id, balance=0)

    payment = Payment(amount=amount)
    payment.create()
    await state.update_data(amount=amount)
    await call.message.delete()
    await call.message.answer(f"Скидка успешна применена. Поздравляю!\n"
                              f"Вы выбрали товар: <b>{data.get('name_item')}</b>\n"
                              f"Количество товара: <b>{data.get('count')}</b>\n"
                              f"Сумма к оплате: <code>{amount} BTC</code>\n"
                              f"Оплатите на этот биткойн кошелек: <code>{config.WALLET_BTC}</code>",
                              reply_markup=buy_item_func_end(True))


@dp.callback_query_handler(state=ItemBuy.paid)
async def check_payment(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data.get("count")
    item_id = data.get("item_id")
    name_item = data.get("name_item")
    delivery_address = data.get("delivery_address")

    print(data.get("payment"))
    payment: Payment = data.get("payment")

    try:
        payment.check_payment()

    except NotConfirmed:
        await call.message.answer("Транзакция найдена. Но еще не подтверждена. Попробуйте позже")
        return
    except NoPaymentFound:
        await call.message.answer("Транзакция не найдена.")
        return
    else:
        count_item = tuple(await db.select_count(item_id=int(item_id)))
        count_item = count_item[0] - int(count)
        await db.update_count(item_id=int(item_id), count=count_item)
        await send_message_admin_successful_order(dp=dp, user_id=call.from_user.id,
                                                  user_name=call.from_user.full_name,
                                                  name_item=name_item,
                                                  count=int(count),
                                                  delivery_address=delivery_address)

    await call.message.delete_reply_markup()
    await call.message.edit_text("Успешно оплачено")

    await state.finish()
