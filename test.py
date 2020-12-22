import time
from decimal import Decimal
from unicodedata import decimal

import blockcypher
import requests


# https://free.currconv.com/api/v7/convert?apiKey=
# https://free.currconv.com/api/v7/convert?apiKey=fc73ffa6f42ad6c99898&q=USD_PHP&compact=y

# class NoAction(Exception):
#     pass
#
#
# class ConvertCurrency(object):
#     def __init__(self, token: str, url: str):
#         self.token = token
#         self.url = url
#
#     @staticmethod
#     def _get_values_one(currency, convert):
#         value = currency[f"{convert}"]["val"]
#         # {'val': 4.3590914e-05}
#         return value
#
#     @staticmethod
#     def _convert_values_count(count, value, multiply=False, divide=False):
#
#         if multiply:
#             value_n = value * count
#         elif divide:
#             value_n = count / value
#         else:
#             raise NoAction
#
#         return value_n
#
#     def convert_currency(self,
#                          from_currency,
#                          to_currency,
#                          count=1,
#                          multiply=False,
#                          divide=False):
#
#         from_to = f"{from_currency}_{to_currency}"
#         post = f"https://free.currconv.com/api/v7/convert?apiKey={self.token}&q={from_to}&compact=y"
#         result_course = requests.get(post)
#         get_values_one = self._get_values_one(result_course.json(),
#                                              from_to)
#         value = self._convert_values_count(count, get_values_one,
#                                           multiply, divide)
#
#         return value
#
#
# cvc = ConvertCurrency(token="fc73ffa6f42ad6c99898",
#                       url="https://free.currconv.com/api/v7/convert?apiKey=")


import math

# math.e 	2.184e-9

a = f"{2.36e-06:.12f}"
print(a)
