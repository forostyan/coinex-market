from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.keyboards import client_kb
from telegram_bot.utils.injector import injector

dp = injector.get("tg_dispatcher")


# ввод состояния
class FSMDeposit(StatesGroup):
    coin = State()
    address = State()


# вывод состояния
class FSMWithdraw(StatesGroup):
    coin = State()
    summ = State()
    address = State()


# создание сделки состояния
class FSMCreate(StatesGroup):
    side = State()
    coin = State()
    fiat = State()
    address = State()
    min = State()
    max = State()
    rate = State()


# выбор сделки состояния
class FSMChoose(StatesGroup):
    side = State()
    coin = State()


# стартовый экран
@dp.message_handler(commands=["start"])
@injector.inject
async def process_start_command(message: types.Message, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT id
            FROM public."user"
            WHERE id='{message.from_user.id}';"""
        )
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                f"""INSERT INTO public."user"
                (id, nickname)
                VALUES('{message.from_user.id}', '{message.from_user.username}');"""
            )
            await message.answer("Ваш личный кабинет был успешно создан")
    db_connection.commit()
    await message.answer(
        "Привет!\nЭто бот CoinMarketEx. Пока в разработке, так что часть функционала недоступна.\n"
        + "Сейчас недоступны:\n Взаимодействие с чужими сделками(обмен 2 пользователей). Хорошего нового года!",
        reply_markup=client_kb.inline_start_kb,
    )


# назад на стартовый экран
@dp.callback_query_handler(text="back btn", state="*")
async def process_callback_back_btn(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Привет!\nЭто бот CoinMarketEx. Пока в разработке, так что бОльшая часть функционала недоступна.\n"
        + "Сейчас недоступны:\n -ввод сумм и адресов кошельков, тк еще нет баз данных.\n "
        + "-Аккаунты и регистрация(по тем же причинам)",
        reply_markup=client_kb.inline_start_kb,
    )
    await state.finish()
    await callback.message.delete()
    await callback.answer()


# кошелек
@dp.callback_query_handler(text="wallet btn")
async def process_callback_wallet_btn(callback: types.CallbackQuery, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
                    SELECT btc, eth, bnb, usdt, usdc, busd
                    FROM public."user"
                    WHERE id='{callback.from_user.id}';"""
        )
        data = list(cursor.fetchone())
    await callback.message.answer(
        "Ваш баланс:\n"
        + f"BTC: {data[0]}\n"
        + f"ETH: {data[1]}\n"
        + f"BNB: {data[2]}\n"
        + f"USDT: {data[3]}\n"
        + f"USDC: {data[4]}\n"
        + f"BUSD: {data[5]}\n"
        + "\n\n"
        + "Также есть возможность ввести/вывести средства",
        reply_markup=client_kb.inline_wallet_kb,
    )
    await callback.message.delete()
    await callback.answer()


# ввод выбор монеты
@dp.callback_query_handler(text="deposit btn")
async def process_callback_deposit_btn(callback: types.CallbackQuery):
    await FSMDeposit.coin.set()
    await callback.message.answer("Выберите монету", reply_markup=client_kb.coins_kb)
    await callback.message.delete()
    await callback.answer()


# ввод конец
@dp.callback_query_handler(state=FSMDeposit.coin)
async def process_callback_deposit_btn(callback: types.CallbackQuery, db_connection):
    await callback.message.answer(
        "Вот кошелек для перевода суммы: [кошельки пока не созданы]\n"
        + f"{callback.data}\n"
        + "Сумма переведенная на этот кошелек будет зачисленна на кошелек пользователя (по дефолту пополняет на 10)",
        reply_markup=client_kb.back_kb,
    )
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
                    SELECT {callback.data}
                    FROM public."user"
                    WHERE id='{callback.from_user.id}';"""
        )
        cur_balance = float(list(cursor.fetchone())[0])
        cursor.execute(
            f"""UPDATE
        public."user"
        SET
        {callback.data} = {cur_balance + 10}
        WHERE
        id = '{callback.from_user.id}';"""
        )
        db_connection.commit()
    await callback.message.delete()
    await callback.answer()


# вывод выбор монеты
@dp.callback_query_handler(text="withdraw btn")
async def process_callback_withdraw_btn(callback: types.CallbackQuery):
    await FSMWithdraw.coin.set()
    await callback.message.answer("Выберите монету", reply_markup=client_kb.coins_kb)
    await callback.message.delete()
    await callback.answer()


# вывод сумма
@dp.callback_query_handler(state=FSMWithdraw.coin)
async def process_callback_withdraw_coin_btn(
        callback: types.CallbackQuery, state: FSMContext
):
    async with state.proxy() as withdraw_data:
        withdraw_data["coin"] = callback.data
    await FSMWithdraw.next()
    await callback.message.answer("Введите сумму")
    await callback.message.delete()
    await callback.answer()


# вывод кошелек
@dp.message_handler(state=FSMWithdraw.summ)
async def process_callback_withdraw_sum_btn(message: types.Message, state: FSMContext):
    async with state.proxy() as withdraw_data:
        withdraw_data["summ"] = message.text
    await FSMWithdraw.next()
    await message.answer("Введите адрес")
    await message.delete()


# вывод конец
@dp.message_handler(state=FSMWithdraw.address)
async def process_callback_withdraw_address_btn(
        message: types.Message, state: FSMContext, db_connection
):
    async with state.proxy() as withdraw_data:
        withdraw_data["address"] = message.text
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
                       SELECT {withdraw_data['coin']}
                       FROM public."user"
                       WHERE id='{message.from_user.id}';"""
        )
        cur_balance = float(list(cursor.fetchone())[0])
        if cur_balance < float(withdraw_data["summ"]):
            await message.answer(
                f"На вашем счету недостаточно средств", reply_markup=client_kb.back_kb
            )
        else:
            cursor.execute(
                f"""UPDATE
               public."user"
               SET
               {withdraw_data['coin']} = {cur_balance - float(withdraw_data['summ'])}
               WHERE
               id = '{message.from_user.id}';"""
            )
            db_connection.commit()
            cursor.execute(
                f"""INSERT INTO public.withdraw
                            (id, userid, address, "time", coin, amount)
                            VALUES('{hash(datetime.now())}', '{message.from_user.id}', '{withdraw_data['address']}', '{datetime.now()}', '{withdraw_data['coin']}', '{withdraw_data['summ']}');"""
            )
            await message.answer(
                f'Введенная сумма будет переведена на выбранный адрес {withdraw_data["address"]}',
                reply_markup=client_kb.back_kb,
            )

            db_connection.commit()
    await message.delete()


# создать сделку
@dp.callback_query_handler(text="create deal btn")
async def process_callback_create_deal_btn(callback: types.CallbackQuery):
    await FSMCreate.side.set()
    await callback.message.answer(
        "Купить или продать криптовалюту?", reply_markup=client_kb.inline_create_deal_kb
    )
    await callback.message.delete()
    await callback.answer()


# создание Выбрать криптовалюту
@dp.callback_query_handler(state=FSMCreate.side)
async def process_callback_create_buy_btn(
        callback: types.CallbackQuery, state: FSMContext
):
    async with state.proxy() as data:
        data["side"] = callback.data
    await FSMCreate.next()
    await callback.message.answer(
        "Выберите криптовалюту", reply_markup=client_kb.coins_kb
    )
    await callback.message.delete()
    await callback.answer()


# создание Выбрать фиат
@dp.callback_query_handler(state=FSMCreate.coin)
async def process_callback_create_coin_btn(
        callback: types.CallbackQuery, state: FSMContext
):
    async with state.proxy() as data:
        data["coin"] = callback.data
    await FSMCreate.next()
    await callback.message.answer(
        "Выберите фиат", reply_markup=client_kb.inline_create_fiat_kb
    )
    await callback.message.delete()
    await callback.answer()


# создание Ввести адрес
@dp.callback_query_handler(state=FSMCreate.fiat)
async def process_callback_create_fiat_btn(
        callback: types.CallbackQuery, state: FSMContext
):
    async with state.proxy() as data:
        data["fiat"] = callback.data
    await FSMCreate.next()
    await callback.message.answer(
        "Введите адрес на который пользователи будут отправлять вам валюту(номер телефона если вы продаете крипту, адрес кошелька если вы покупаете крипту)"
    )
    await callback.message.delete()
    await callback.answer()


# создание ввести минимум валюты
@dp.message_handler(state=FSMCreate.address)
async def process_callback_create_address_btn(
        message: types.Message, state: FSMContext
):
    async with state.proxy() as data:
        data["address"] = message.text
    await FSMCreate.next()
    await message.answer("Введите Минимум валюты")
    await message.delete()


# создание ввести максимум валюты
@dp.message_handler(state=FSMCreate.min)
async def process_callback_create_min_btn(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["min"] = message.text
    await FSMCreate.next()
    await message.answer("Введите максимум валюты)")
    await message.delete()


# создание ввести курс
@dp.message_handler(state=FSMCreate.max)
async def process_callback_create_max_btn(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["max"] = message.text
        if float(data["max"]) < float(data["min"]):
            data["max"], data["min"] = data["min"], data["max"]
    await FSMCreate.next()
    await message.answer("Введите курс")
    await message.delete()


# создание конец
@dp.message_handler(state=FSMCreate.rate)
async def process_callback_create_rate_btn(
        message: types.Message, state: FSMContext, db_connection
):
    async with state.proxy() as data:
        data["rate"] = message.text
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
                       SELECT {data['coin']}
                       FROM public."user"
                       WHERE id='{message.from_user.id}';"""
        )
        cur_balance = float(list(cursor.fetchone())[0])
        buyer, buyer_name, seller, seller_name = "", "", "", ""
        if data["side"] == "buy":
            buyer = message.from_user.id
            buyer_name = message.from_user.username
        else:
            seller = message.from_user.id
            seller_name = message.from_user.username
        if cur_balance < float(data["max"]) and data["side"] == "sell":
            await message.answer(
                f"На вашем счету недостаточно средств для создания сделки",
                reply_markup=client_kb.back_kb,
            )
        else:
            cursor.execute(
                f"""INSERT INTO public."order"
                            (id, "time", seller, seller_name, buyer, buyer_name, coin, rate, min, max, fiat, status)
                            VALUES('{hash(datetime.now())}', '{datetime.now()}', '{seller}', '{seller_name}', '{buyer}', '{buyer_name}', '{data['coin']}', {data['rate']}, {data['min']}, {data['max']}, '{data['fiat']}', 'created');
                            """
            )
            db_connection.commit()

    async with state.proxy() as data:
        await message.answer(
            f'Создана сделка:\n {data["side"]}\n'
            + f'от {data["min"]} до {data["max"]} валюты {data["coin"]}\n'
            + f'по курсу {data["rate"]}\n',
            reply_markup=client_kb.back_kb,
        )
    await message.delete()


# выбрать сделку
@dp.callback_query_handler(text="take deal btn")
async def process_callback_take_btn(callback: types.CallbackQuery):
    await FSMChoose.side.set()
    await callback.message.answer(
        "Купить или продать криптовалюту?", reply_markup=client_kb.inline_take_kb
    )
    await callback.message.delete()
    await callback.answer()


# выбрать выбор монеты
@dp.callback_query_handler(state=FSMChoose.side)
async def process_callback_take_buy_btn(
        callback: types.CallbackQuery, state: FSMContext
):
    async with state.proxy() as data:
        data["side"] = callback.data
    await FSMChoose.next()
    await callback.message.answer(
        "Выберите криптовалюту.", reply_markup=client_kb.coins_kb
    )
    await callback.message.delete()
    await callback.answer()


# выбрать конец
@dp.callback_query_handler(state=FSMChoose.coin)
async def process_callback_take_coin_btn(
        callback: types.CallbackQuery, state: FSMContext, db_connection
):
    async with state.proxy() as data:
        data["coin"] = callback.data
    msg = "Вот доступные сделки по вашему запросу:\n"
    if data["side"] == "buy":
        partner = "seller"
    else:
        partner = "buyer"
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
                               SELECT seller_name||'; '||buyer_name||'; '||coin||'; '||rate||'; '||min||'; '||max||'; '||fiat
                               FROM public."order"
                               WHERE {partner}!= '' and coin = '{data['coin']}';"""
        )
        result = cursor.fetchone()
        if result:
            for row in result:
                dt = row.split("; ")
                msg += f"Продавец - {dt[0]}, Покупатель - {dt[1]}, Монета - {dt[2]}, Фиат - {dt[6]}, Курс - {dt[3]}, Минимум - {dt[4]}, Максимум - {dt[5]}\n\n"
        else:
            msg += "Доступных сделок нет!"
    await callback.message.answer(msg, reply_markup=client_kb.back_kb)
    await callback.message.delete()
    await callback.answer()


# мои сделки
@dp.callback_query_handler(text="my deals btn")
async def process_callback_my_deals_btn(callback: types.CallbackQuery):
    await callback.message.answer(
        "Выберите тип сделок", reply_markup=client_kb.inline_deals_kb
    )
    await callback.message.delete()
    await callback.answer()


# активные сделки
@dp.callback_query_handler(text="my active btn")
async def process_callback_my_active_btn(callback: types.CallbackQuery, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            f"""
                       SELECT seller_name||'; '||buyer_name||'; '||coin||'; '||rate||'; '||min||'; '||max||'; '||fiat
                       FROM public."order"
                       WHERE buyer = '{callback.from_user.id}' or seller = '{callback.from_user.id}';"""
        )
        result = cursor.fetchone()
        msg = "Тут будут отображены активные сделки:\n"
        if result:
            for row in result:
                dt = row.split("; ")
                msg += f"Продавец - {dt[0]}, Покупатель - {dt[1]}, Монета - {dt[2]}, Фиат - {dt[6]}, Курс - {dt[3]}, Минимум - {dt[4]}, Максимум - {dt[5]}\n\n"
        else:
            msg += "Активных сделок нет!"
    await callback.message.answer(msg, reply_markup=client_kb.back_kb)
    await callback.message.delete()
    await callback.answer()


# закрытые сделки
@dp.callback_query_handler(text="my closed btn")
async def process_callback_my_closed_btn(callback: types.CallbackQuery):
    await callback.message.answer(
        "Закрытых сделок пока нет(тк. взаимодействие пока недоступно)",
        reply_markup=client_kb.back_kb,
    )
    await callback.message.delete()
    await callback.answer()


@injector.inject
def register_handlers_client(tg_dispatcher: Dispatcher):
    tg_dispatcher.register_message_handler(process_start_command, commands=["start"])
    tg_dispatcher.register_callback_query_handler(process_start_command)
    tg_dispatcher.register_callback_query_handler(process_callback_back_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_wallet_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_deal_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_my_deals_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_my_active_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_my_closed_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_deposit_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_withdraw_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_withdraw_coin_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_withdraw_sum_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_withdraw_address_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_buy_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_coin_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_fiat_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_address_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_min_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_max_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_create_rate_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_take_buy_btn)
    tg_dispatcher.register_callback_query_handler(process_callback_take_coin_btn)
