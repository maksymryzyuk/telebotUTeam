from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Request, async_session

async def add_user(telegram_id, lastname, firstname, number, password):
    async with async_session() as session:
        async with session.begin():
            user = User(
                telegram_id=telegram_id,
                lastname=lastname,
                firstname=firstname,
                number=number,
                password=password
            )
            session.add(user)

async def get_user_by_number(number):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.number == number))
        return result.scalars().first()

async def get_user_by_id(telegram_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalars().first()

async def update_balance(telegram_id, amount):
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_id(telegram_id)
            if user:
                if user.balance is None:
                    user.balance = 0.0  # Якщо balance None, ініціалізуємо його нулем
                user.balance += amount  # Оновлюємо баланс
                await session.commit()
                return user.balance
    return None

async def update_tariff(telegram_id, tariff_name):
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_id(telegram_id)
            if user:
                user.tariff = tariff_name  # Оновлюємо тариф у користувача
                await session.commit()

async def add_request(user_id, queue_number):
    async with async_session() as session:
        async with session.begin():
            request = Request(user_id=user_id, queue_number=queue_number)
            session.add(request)

async def get_request_by_user(user_id):
    async with async_session() as session:
        result = await session.execute(select(Request).where(Request.user_id == user_id))
        return result.scalars().first()

async def delete_request(user_id):
    async with async_session() as session:
        async with session.begin():
            request = await get_request_by_user(user_id)
            if request:
                await session.delete(request)
                await session.commit()