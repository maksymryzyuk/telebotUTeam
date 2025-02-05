import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from database.models import async_db

bot = Bot(token = TOKEN)
dp = Dispatcher()

async def main():
    await async_db()  # Ініціалізація бази даних
    dp.include_router(router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

async def on_startup():
    print("Bot ON")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot OFF")