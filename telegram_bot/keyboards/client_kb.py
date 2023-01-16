from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

back_btn = InlineKeyboardButton("Отмена", callback_data="back btn")

back_kb = InlineKeyboardMarkup().add(back_btn)

# стартовый экран
wallet_btn = InlineKeyboardButton("Мой кошелек", callback_data="wallet btn")  # <
my_deals_btn = InlineKeyboardButton("Мои сделки", callback_data="my deals btn")  # <
create_btn = InlineKeyboardButton(
    "Создать сделку", callback_data="create deal btn"
)  # <
take_deal_btn = InlineKeyboardButton(
    "Выбрать сделку", callback_data="take deal btn"
)  # <
inline_start_kb = (
    InlineKeyboardMarkup().row(wallet_btn, my_deals_btn).row(create_btn, take_deal_btn)
)

# кошелек
deposit_btn = InlineKeyboardButton("Ввести средства", callback_data="deposit btn")
withdraw_btn = InlineKeyboardButton("Вывести средства", callback_data="withdraw btn")
inline_wallet_kb = (
    InlineKeyboardMarkup().add(deposit_btn).add(withdraw_btn).add(back_btn)
)


# ввод выбор монет
btc = InlineKeyboardButton("BTC", callback_data="btc")
eth = InlineKeyboardButton("ETH", callback_data="eth")
bnb = InlineKeyboardButton("BNB", callback_data="bnb")
usdt = InlineKeyboardButton("USDT", callback_data="usdt")
usdc = InlineKeyboardButton("USDC", callback_data="usdc")
busd = InlineKeyboardButton("BUSD", callback_data="busd")
coins_kb = (
    InlineKeyboardMarkup()
    .add(btc)
    .add(eth)
    .add(bnb)
    .add(usdt)
    .add(usdc)
    .add(busd)
    .add(back_btn)
)
# вывод выбор монеты
withdraw_coin_btn = InlineKeyboardButton("BTC", callback_data="withdraw coin btn")
inline_withdraw_coins_kb = InlineKeyboardMarkup().add(withdraw_coin_btn)
# вывод сумма
withdraw_sum_btn = InlineKeyboardButton(
    "[ввод суммы]", callback_data="withdraw sum btn"
)
inline_withdraw_sum_kb = InlineKeyboardMarkup().add(withdraw_sum_btn)
# вывод кошелек
withdraw_address_btn = InlineKeyboardButton(
    "[ввод адреса]", callback_data="withdraw address btn"
)
inline_withdraw_address_kb = InlineKeyboardMarkup().add(withdraw_address_btn)


# создать сделку
create_buy_btn = InlineKeyboardButton("Купить", callback_data="buy")
create_sell_btn = InlineKeyboardButton("Продать", callback_data="sell")
inline_create_deal_kb = (
    InlineKeyboardMarkup().row(create_buy_btn, create_sell_btn).add(back_btn)
)
# создание выбор криптовалюты
create_coin_btn = InlineKeyboardButton("BTC", callback_data="create coin btn")
inline_create_coins_kb = InlineKeyboardMarkup().add(create_coin_btn)
# создание выбрать фиат
create_fiat_btn = InlineKeyboardButton("RUB (Тинькофф)", callback_data="tinkoff rub")
inline_create_fiat_kb = InlineKeyboardMarkup().add(create_fiat_btn)
# создание ввести адрес
create_address_btn = InlineKeyboardButton(
    "[Ввести телефон/адрес]", callback_data="create address btn"
)
inline_create_address_kb = InlineKeyboardMarkup().add(create_address_btn)
# создание ввести минимум валюты
create_min_btn = InlineKeyboardButton(
    "[Ввести минимум]", callback_data="create min btn"
)
inline_create_min_kb = InlineKeyboardMarkup().add(create_min_btn)
# создание ввести максимум валюты
create_max_btn = InlineKeyboardButton(
    "[Ввести максимум]", callback_data="create max btn"
)
inline_create_max_kb = InlineKeyboardMarkup().add(create_max_btn)
# создание ввести курс
create_rate_btn = InlineKeyboardButton("[Ввести курс]", callback_data="create rate btn")
inline_create_rate_kb = InlineKeyboardMarkup().add(create_rate_btn)

# выбрать сделку
take_buy_btn = InlineKeyboardButton("Купить", callback_data="buy")
take_sell_btn = InlineKeyboardButton("Продать", callback_data="sell")
inline_take_kb = InlineKeyboardMarkup().row(take_buy_btn, take_sell_btn).add(back_btn)
# выбрать выбор монеты
take_coin_btn = InlineKeyboardButton("BTC", callback_data="take coin btn")
inline_take_coins_kb = InlineKeyboardMarkup().add(take_coin_btn)

# мои сделки
active_deals_btn = InlineKeyboardButton(
    "Активные сделки", callback_data="my active btn"
)
closed_deals_btn = InlineKeyboardButton(
    "Закрытые сделки", callback_data="my closed btn"
)
inline_deals_kb = (
    InlineKeyboardMarkup().row(active_deals_btn, closed_deals_btn).add(back_btn)
)
