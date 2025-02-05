from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from database.requests import *

router = Router()

class Reg(StatesGroup):
    lastname = State()
    firstname = State()
    number = State()
    password = State()

class Login(StatesGroup):
    number = State()
    password = State()

class TopUp(StatesGroup):
    amount = State()

class SelectTariff(StatesGroup):
    tariff = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Вітаємо! Натисніть /help для деталей або напишіть запитання!", reply_markup=kb.main)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("Ось список команд:\n/login - Вхід\n/reg - Реєстрація")

@router.message(F.text == "📝 Зареєструватися")
@router.message(Command('reg'))
async def reg_start(message: Message, state: FSMContext):
    await state.set_state(Reg.lastname)
    await message.answer("Введіть своє прізвище:", reply_markup=ReplyKeyboardRemove())

@router.message(Reg.lastname)
async def reg_lastname(message: Message, state: FSMContext):
    await state.update_data(lastname=message.text)
    await state.set_state(Reg.firstname)
    await message.answer("Введіть своє ім'я:")

@router.message(Reg.firstname)
async def reg_firstname(message: Message, state: FSMContext):
    await state.update_data(firstname=message.text)
    await state.set_state(Reg.number)
    await message.answer("Введіть номер телефону:")

@router.message(Reg.number)
async def reg_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(Reg.password)
    await message.answer("Введіть пароль:")

@router.message(Reg.password)
async def reg_password(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_user(message.from_user.id, data["lastname"], data["firstname"], data["number"], message.text)
    await message.answer("✅ Реєстрація успішна!", reply_markup=kb.main)
    await state.clear()

@router.message(F.text == "🔑 Авторизація")
@router.message(Command('login'))
async def login_start(message: Message, state: FSMContext):
    await state.set_state(Login.number)
    await message.answer("📲 Введіть номер телефону:")

@router.message(Login.number)
async def login_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(Login.password)
    await message.answer("🔑 Введіть пароль:")

@router.message(Login.password)
async def login_password(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await get_user_by_number(data["number"])
    if user and user.password == message.text:
        await message.answer(f"✅ Вхід успішний! Вітаємо, {user.firstname}!", reply_markup=kb.user_menu)
        await state.clear()
    else:
        await message.answer("❌ Невірний номер або пароль.")

@router.message(F.text == "💰 Переглянути баланс")
async def view_balance(message: Message):
    user = await get_user_by_id(message.from_user.id)

    if user:
        tariff_name = user.tariff
        balance = user.balance if user.balance is not None else 0
        await message.answer(f"📜 Ваш тариф: {tariff_name}\n💳 Поточний баланс: {balance} грн.",
                             reply_markup=kb.balance_menu)
    else:
        await message.answer("❌ Не знайдено вашого акаунту. Виконайте авторизацію або реєстрацію.")

@router.message(F.text == "💳 Поповнити баланс")
async def top_up_start(message: Message, state: FSMContext):
    await state.set_state(TopUp.amount)
    await message.answer("💳 Введіть суму поповнення:")

@router.message(TopUp.amount)
async def top_up_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        new_balance = await update_balance(message.from_user.id, amount)
        await message.answer(f"✅ Баланс поповнено. Поточний баланс: {new_balance} грн.", reply_markup=kb.balance_menu)
        await state.clear()
    except:
        await message.answer("❌ Невірний формат суми.")

@router.message(F.text == "🔙 Назад")
async def back_to_user_menu(message: Message):
    await message.answer("🔙 Повернення до меню", reply_markup=kb.user_menu)

@router.message(F.text == "📜 Тарифи")
async def show_tariffs(message: Message):
    await message.answer("📜 Оберіть тариф:", reply_markup=kb.tariff_menu)

@router.callback_query(F.data.startswith("tariff_"))
async def tariff_selected(callback: CallbackQuery, state: FSMContext):
    tariffs_info = {
        "tariff_100": ("Інтернет 100 Мбіт/с", 150),
        "tariff_200": ("Інтернет 200 Мбіт/с", 200),
        "tariff_500": ("Інтернет 500 Мбіт/с", 300),
        "tariff_100_tv": ("Інтернет 100 Мбіт/с + Телебачення", 250),
        "tariff_500_tv": ("Інтернет 500 Мбіт/с + Телебачення", 400),
    }

    tariff_data = tariffs_info.get(callback.data)
    if tariff_data:
        tariff_name, tariff_price = tariff_data
        await callback.message.answer(
            f"📜 <b>{tariff_name}</b>\n💵 <b>Ціна:</b> {tariff_price} грн/міс\n✅ Обрати цей тариф?",
            parse_mode="HTML",
            reply_markup=kb.tariff_reply_menu
        )
        await callback.answer()
        await state.update_data(selected_tariff=(tariff_name, tariff_price))
    else:
        await callback.message.answer("❌ Невідомий тариф.")
        await callback.answer()

@router.message(F.text == "✅ Обрати")
async def confirm_tariff(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)

    if user:
        data = await state.get_data()
        selected_tariff = data.get("selected_tariff")

        if selected_tariff:
            tariff_name, tariff_price = selected_tariff
            user.tariff = tariff_name  # Оновлюємо тариф у базі
            await update_balance(user.telegram_id, -tariff_price)  # Віднімаємо суму з балансу
            await update_tariff(user.telegram_id, tariff_name)  # Оновлюємо тариф у базі

            await message.answer(f"✅ Ви успішно обрали тариф: {tariff_name}.\n💵 Місячна плата: {tariff_price} грн.",
                                 reply_markup=kb.user_menu)
            await state.clear()
        else:
            await message.answer("❌ Ви ще не вибрали тариф.")
    else:
        await message.answer("❌ Не знайдено вашого акаунту. Виконайте авторизацію або реєстрацію.")

@router.message(F.text == "🛠 Інші послуги")
async def other_services(message: Message):
    await message.answer("Оберіть послугу:", reply_markup=kb.services_menu)

@router.message(F.text == "📡 Підключення")
async def connection_services(message: Message):
    user = await get_user_by_id(message.from_user.id)
    request = await get_request_by_user(user.id)

    if request:
        await message.answer("📡 Ви вже подали заявку на підключення.\n❌ Якщо потрібно, ви можете її відмінити.",
                             reply_markup=kb.cancel_request_menu)
    else:
        await message.answer("📡 Ви можете залишити заявку на підключення.", reply_markup=kb.connection_menu)

@router.message(F.text == "📝 Залишити заявку на підключення")
async def leave_request(message: Message):
    user = await get_user_by_id(message.from_user.id)

    if not await get_request_by_user(user.id):
        queue_number = (await get_request_by_user(user.id)) or 1
        await add_request(user.id, queue_number)

        await message.answer(f"✅ Ваша заявка прийнята!\n📌 Ваш номер у черзі: {queue_number}",
                             reply_markup=kb.cancel_request_menu)
    else:
        await message.answer("❌ Ви вже подали заявку!", reply_markup=kb.cancel_request_menu)

@router.message(F.text == "❌ Відмінити заявку")
async def cancel_request(message: Message):
    user = await get_user_by_id(message.from_user.id)
    request = await get_request_by_user(user.id)

    if request:
        await delete_request(user.id)
        await message.answer("❌ Ваша заявка скасована.", reply_markup=kb.connection_menu)
    else:
        await message.answer("❌ У вас немає активної заявки.", reply_markup=kb.connection_menu)

@router.message(F.text == "🚪 Вийти з кабінету")
async def logout(message: Message):
    await message.answer("🚪 Ви вийшли з кабінету.", reply_markup=kb.main)