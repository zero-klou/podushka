from aiogram import executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import load_config
from common_handlers import register_handlers_common
import logging

logging.basicConfig(level=logging.INFO)

config = load_config('bot.ini')

bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers_common(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)