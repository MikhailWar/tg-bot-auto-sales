import logging
import re

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.deep_linking import get_start_link

from data.config import admins
from filters import IsNotRefferal
from keyboards.inline import generation_random_call_inline_mode
from loader import dp, db

@dp.message_handler(IsNotRefferal(), lambda msg: msg.text.isdigit())
async def start_bot_to_add_refferal_manual(message: types.Message):
    id_referral = message.text
    massive_all_users = [users[0] for users in await db.select_all_users]
    link_refferal= await get_start_link(f"{admins[0]}")

    if int(id_referral) in massive_all_users:
        if message.from_user.id == int(id_referral) and message.from_user.id not in admins:
            return
        telegram_link_refferal = f"tg://user?id={id_referral}"
        await db.update_user_id_reffer(id_refer=int(id_referral), user_id=message.from_user.id)
        await db.update_balance(user_id=int(id_referral))
        await message.answer(f"Вы добавлены, <a href='{telegram_link_refferal}'>ваш реффер</a>",
                             reply_markup=generation_random_call_inline_mode("Курс"))

    else:
        await message.answer(f"Введен неправильный код доступа.\n"
                             f"Если у вас нет кода от реферала. Воспользуйтесь ссылкой - <a href = '{link_refferal}'>нажми на меня</a>")

@dp.message_handler(IsNotRefferal(),
                    CommandStart(re.compile(r"(start)?(\d+)"))
                    )
async def start_bot_to_add_refferal(message: types.Message):
    print("sas")
    referral = int(message.get_args())
    massive_all_users = [users[0] for users in await db.select_all_users]
    link_refferal= await get_start_link(f"{admins[0]}")

    if int(referral) in massive_all_users:
        if message.from_user.id == int(referral) and message.from_user.id not in admins:
            return
        telegram_link_referral = f"tg://user?id={referral}"
        await db.update_user_id_reffer(id_refer=referral, user_id=message.from_user.id)
        await db.update_balance(user_id=referral)
        logging.info("Мы обновили данные в базе данных. айди реферала, баланс для реферала")
        await message.answer(f"Вы добавлены, <a href='{telegram_link_referral}'>ваш реферал</a>",
                             reply_markup=generation_random_call_inline_mode(""))
    else:
        await message.answer(f"Неправильная ссылка приглашения.\n"
                             f"Перейдите по этой ссылке, чтобы зарегистрироваться <a href='{link_refferal}'>зарегистрироваться</a> ")
