import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    483200140
]
bot_id = 1495205697

files_id = []
ip = os.getenv("ip")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
database = os.getenv("database")

TOKEN_CONVERT = os.getenv("TOKEN_CONVERT")
URL_CONVERT = os.getenv("URL_CONVERT")

BLOCKCYPER_TOKEN = os.getenv("BLOCKCYPER_TOKEN")
WALLET_BTC = os.getenv("WALLET_BTC")
REQUEST_LINK = "bitcoin:{address}?" \
               "amount={amount}" \
               "&label={message}"

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
