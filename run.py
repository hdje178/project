import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await bot.set_my_commands([
        {"command": "start", "description": "Запустити бота"},
        {"command": "help", "description": "Допомога"},
        {"command": "get_photo", "description": "Отримати фото"}
    ])
    
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:    
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")