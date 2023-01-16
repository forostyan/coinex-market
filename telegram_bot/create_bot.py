import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=os.getenv("TOKEN"))  # поменять на нужный
dp = Dispatcher(bot, storage=storage)
