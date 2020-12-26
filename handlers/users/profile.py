from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.deep_linking import get_start_link

from keyboards.inline import generation_random_call_inline_mode
from loader import dp, db, con_currency, bot


@dp.message_handler(Command("get_profile"))
async def conclusion_information(message: types.Message):
    balance = tuple(await db.select_balance(user_id=message.from_user.id))
    refferal_link = await get_start_link(message.from_user.id)

    count_referrals = tuple(await db.how_many_a_referrals(user_id=message.from_user.id))
    balance_btc = await con_currency.convert_currency(
        from_currency="USD",
        to_currency="BTC",
        count=balance[0],
        multiply=True
    )

    text = f"""
ID - <b>{message.from_user.id}</b>
Имя - <b>{message.from_user.full_name}</b>
Юзернейм - <b>{message.from_user.username}</b>
Ваш баланс - <b>{balance[0]:.2f}$</b> <code>{balance_btc:.12f} BTC</code>
Рефералы - <b>{count_referrals[0]}</b>
--------------------------------
За привлечение нового пользователя бота, вам начисляется 10 баллов = 10$
Ваша реферальная ссылка: 
<code>{refferal_link}</code>
Ваш реферальный код: <code>{message.from_user.id}</code>

    """
    await message.answer(text=text,
                         reply_markup=generation_random_call_inline_mode(""))
