import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from data.config import TOKEN_CONVERT, URL_CONVERT

from utils.db_api import DataBase
from utils.misc import ConvertCurrency

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()
db = loop.run_until_complete(DataBase.create())
con_currency = ConvertCurrency(token=TOKEN_CONVERT, url = URL_CONVERT)


