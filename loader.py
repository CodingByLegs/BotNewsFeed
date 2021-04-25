from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from telethon.sync import TelegramClient

from data import config

api_id = config.API_ID
api_hash = config.API_HASH
username = config.USERNAME

client = TelegramClient(username, api_id, api_hash)
client.start()

storage = RedisStorage(config.IP, config.PORT, db=5)

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
