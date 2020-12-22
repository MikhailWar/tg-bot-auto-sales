from aiogram.dispatcher.filters.state import StatesGroup, State


class ItemBuy(StatesGroup):
    count = State()
    delivery_address = State()
    paid = State()