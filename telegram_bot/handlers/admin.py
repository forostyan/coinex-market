from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from telegram_bot.utils.injector import injector

dp = injector.get("tg_dispatcher")


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(commands="Загрузить", state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply("Загрузи фото")
