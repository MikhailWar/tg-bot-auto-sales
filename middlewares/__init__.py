from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher) -> object:
    dp.middleware.setup(ThrottlingMiddleware())
