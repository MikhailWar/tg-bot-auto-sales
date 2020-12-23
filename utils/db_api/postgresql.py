import logging

import asyncpg
from asyncpg.pool import Pool

from data.config import PGUSER, PGPASSWORD, ip


class DataBase(object):
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=PGUSER,
            password=PGPASSWORD,
            host=ip
        )
        return cls(pool)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        user_id INT NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        id_refer INT,
        balance INT default 0,
        PRIMARY KEY (user_id)
        )
        """
        return await self.pool.execute(sql)

    async def create_table_items(self):
        sql = """
        CREATE TABLE IF NOT EXISTS items(
        id_item INT,
        name varchar(255),
        description varchar(4000),
        price decimal,
        price_btc decimal,
        photo varchar(255),
        currency varchar(255),
        count integer
        )
        """
        return await self.pool.execute(sql)

    async def add_user(self, user_id: int, full_name: str):
        try:
            sql = "INSERT INTO users (user_id, full_name) VALUES ($1, $2)"
            return await self.pool.execute(sql, user_id, full_name)
        except:
            pass

    async def add_item_base(self, value: tuple):
        sql = "INSERT INTO items (id_item, name, description, price, photo, currency,  price_btc, count) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)"
        return await self.pool.execute(sql, *value)

    async def select_id_refer_user(self, user_id: int):
        sql = "SELECT id_refer FROM users WHERE user_id = $1"
        return await self.pool.fetchval(sql, user_id)

    @property
    async def select_all_users(self):
        sql = "SELECT user_id FROM users"
        return await self.pool.fetch(sql)

    async def update_user_id_reffer(self, id_refer: int, user_id: int):
        sql = "update users SET id_refer = $1 WHERE user_id = $2"
        return await self.pool.execute(sql, id_refer, user_id)

    async def select_balance(self, user_id: int):
        sql = "select balance from users where user_id = $1"
        return await self.pool.fetchrow(sql, user_id)

    async def update_balance(self, user_id: int, balance: int = 10):
        sql = "update users SET balance=$1 WHERE user_id=$2"
        current_balance = tuple(await self.select_balance(user_id))
        balance += current_balance[0]
        logging.info(balance)
        return await self.pool.execute(sql, balance, user_id)

    async def set_balance_user(self, user_id: int, balance: int = 0):
        sql = "update users SET balance=$1 WHERE user_id=$2"
        return await self.pool.execute(sql, balance, user_id)

    async def how_many_a_referrals(self, user_id: int):
        sql = "select count(*) as id_refer from users where id_refer=$1"
        return await self.pool.fetchrow(sql, user_id)


    @staticmethod
    async def format_select_items(sql, name):
        sql+=" ".join([
                f"'{name}%'"
            ])
        return sql

    async def select_items(self, name: str):
        try:
            sql = "select * from items where name like "
            sql = await self.format_select_items(sql, name)

            return await self.pool.fetch(sql)
        except:
            logging.info("Ошибка")

    async def select_count(self, item_id: int):
        sql = "select count from items where id_item = $1"
        return await self.pool.fetchrow(sql, item_id)

    async def update_count(self, item_id: int, count: int):
        sql = "update items set count = $1 where id_item = $2"
        return await self.pool.fetchrow(sql, count, item_id)

    async def select_items_all(self):
        sql = "select*from items"
        return await self.pool.fetch(sql)

    async def select_id_items_all(self):
        sql = "select id_item from items"
        return await self.pool.fetch(sql)

    async def select_name_and_currency_items(self, item_id:int):
        sql = "select name, currency from items where id_item = $1"
        return await self.pool.fetchrow(sql, item_id)

    async def select_name_items(self, name: str):
        sql = "select * from items where name = $1"
        return await self.pool.fetch(sql, name)

    async def select_items_all_where_items_id(self, item_id: int):
        sql = "select * from items where id_item = $1"
        return await self.pool.fetchrow(sql, item_id)