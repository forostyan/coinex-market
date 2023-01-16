from aiogram.utils import executor
from telegram_bot.create_bot import dp
from telegram_bot.handlers import client, admin, other


async def on_startup(_):
    print("Вышел в онлайн")


if __name__ == "__main__":
    client.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
