from decimal import Decimal, getcontext

import aiohttp
import requests


class NoAction(Exception):
    pass


class ConvertCurrency(object):
    def __init__(self, token: str, url: str):
        getcontext().prec = 28 # настройки
        self.token = token
        self.url = url

    @staticmethod
    def _get_values_one(currency, convert):
        value = currency[f"{convert}"]["val"]
        # {'val': 4.3590914e-05}
        return value

    @staticmethod
    def _convert_values_count(count, value, multiply=False, divide=False):

        if multiply:
            value_n = Decimal(f"{value}") * Decimal(f"{count}")
        elif divide:
            value_n = Decimal(f"{count}") / Decimal(f"{value}")
        else:
            raise NoAction

        return value_n

    async def convert_currency(self,
                               from_currency,
                               to_currency,
                               count=1,
                               multiply=False,
                               divide=False):

        from_to = f"{from_currency}_{to_currency}"
        post = f"https://free.currconv.com/api/v7/convert?apiKey={self.token}&q={from_to}&compact=y"

        async with aiohttp.ClientSession() as session:
            result_course = await session.get(post)  # делаем запрос к апи
            result_course = await result_course.json()  # получаем данные в формате JSON
            await session.close()  # закрываем сессию

        get_values_one = self._get_values_one(result_course,
                                              from_to)  # курс валюты за один эквивалиент

        value = self._convert_values_count(count, get_values_one,
                                           multiply, divide)  # конвертация валюты в другую валюту
        return value
