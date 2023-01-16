from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import dp


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Загрузи фото')
