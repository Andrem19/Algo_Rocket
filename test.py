import helpers.tel as tel
from decouple import config
from telegram import Bot
import asyncio

api_token = config('API_TOKEN_1')
chat_id = config("CHAT_ID")

bot = Bot(token=api_token)
message = '<a href="https://www.coingecko.com/en/coins/ethereum">ETH</a>'
asyncio.run(tel.send_inform_message(message, '', False))