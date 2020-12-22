from aiogram import Dispatcher

from filters.admins import IsAdmin
from filters.is_not_from_reffral import IsNotRefferal
from filters.item import CheckItems


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsNotRefferal)
    dp.filters_factory.bind(CheckItems)

