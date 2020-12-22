

# отправка администраторам об успешном заказе
from aiogram import Dispatcher

from data.config import admins



async def send_message_admin_successful_order(dp: Dispatcher,
                                              user_id: int,
                                              user_name: str,
                                              name_item: str,
                                              count: int,
                                              delivery_address: str):

    link = f"tg://user?id={user_id}"
    text = "\n".join([
        "У вас новый заказ!",
        f"От пользователя: <a href='{link}'>{user_name}</a>",
        f"Заказал: {name_item}",
        f"Количество: {count}",
        f"Адрес доставки: {delivery_address}"
    ]
    )

    for admin in admins:
        await dp.bot.send_message(chat_id=admin, text=text)