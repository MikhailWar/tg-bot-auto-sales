from aiogram.dispatcher.filters.state import StatesGroup, State


class AddItem(StatesGroup):
    """
   id_item: int,
   name: str,
   description: str,
   price: int,
   photo: str,
   currency: str = "RUB"
    """
    accept = State()
    id_item = State()
    name = State()
    description = State()
    price = State()
    photo = State()
    currency = State()
    count = State()
    end_accept = State()

