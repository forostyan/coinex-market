from giveme import Injector

__all__ = ("injector",)

injector = Injector()


@injector.register(singleton=True)
def db_settings():
    from dynaconf import Dynaconf

    return Dynaconf(envvar_prefix="POSTGRES", load_dotenv=True)


@injector.register()
@injector.inject
def db_connection(db_settings):
    import psycopg2

    return psycopg2.connect(
        host=db_settings.host,
        user=db_settings.user,
        password=db_settings.password,
        database=db_settings.db,
    )


@injector.register(singleton=True)
def tg_settings():
    from dynaconf import Dynaconf

    return Dynaconf(envvar_prefix="TGBOT", load_dotenv=True)


@injector.register(singleton=True)
@injector.inject
def tg_dispatcher(tg_settings):
    from aiogram.contrib.fsm_storage.memory import MemoryStorage
    from aiogram import Bot
    from aiogram.dispatcher import Dispatcher

    storage = MemoryStorage()

    bot = Bot(token=tg_settings.token)
    return Dispatcher(bot, storage=storage)
