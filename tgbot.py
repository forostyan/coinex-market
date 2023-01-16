from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from telegram_bot.handlers import client
from telegram_bot.utils.injector import injector


async def on_startup(_):
    print("Вышел в онлайн")


@injector.inject
def run(tg_dispatcher: Dispatcher):
    client.register_handlers_client()
    executor.start_polling(tg_dispatcher, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    run()
