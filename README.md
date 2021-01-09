# tg-bot-auto-sales
for automatic sales

<h2>Instruction. How to run a bot in Linux?</h2> 

<b>Clone Repository</b>
- > git clone https://github.com/Maiss-python/tg-bot-auto-sales.git

<b>Create new file .env</b>
- > nano .env

<b>Download database PostgreSQL</b>
- > sudo apt install postgresql

<b>Writing data in file .env</b>
- BOT_TOKEN = You need to get token from Telegram @BotFather
- PGUSER =postgres
- PGPASSWORD = you_password
- BLOCKCYPER_TOKEN = get token https://www.blockcypher.com/
- WALLET_BTC = write your bitcoin adress
- TOKEN_CONVERT = get token https://www.currencyconverterapi.com/
- URL_CONVERT =https://free.currconv.com/api/v7/convert?apiKey=

<b>Run bot Telegram </b>

- > cd tg-bot-auto-sales
- > sudo docker-compose up


<b>Good Luck</b>
