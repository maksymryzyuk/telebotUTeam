from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔑 Авторизація"), KeyboardButton(text="📝 Зареєструватися")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію"
)

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Переглянути баланс")],
        [KeyboardButton(text="📜 Тарифи"), KeyboardButton(text="🛠 Інші послуги")],
        [KeyboardButton(text="🚪 Вийти з кабінету")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію"
)

balance_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 Поповнити баланс")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію"
)

tariff_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📶 Інтернет 100 Мбіт/с", callback_data="tariff_100")],
        [InlineKeyboardButton(text="📶 Інтернет 200 Мбіт/с", callback_data="tariff_200")],
        [InlineKeyboardButton(text="📶 Інтернет 500 Мбіт/с", callback_data="tariff_500")],
        [InlineKeyboardButton(text="📺 Інтернет 100 Мбіт/с + ТБ", callback_data="tariff_100_tv")],
        [InlineKeyboardButton(text="📺 Інтернет 500 Мбіт/с + ТБ", callback_data="tariff_500_tv")]
    ]
)

tariff_reply_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Обрати")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📡 Підключення")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Оберіть дію"
)

connection_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Залишити заявку на підключення")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

cancel_request_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Відмінити заявку")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)
