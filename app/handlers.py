from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import TOKEN
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


import app.keyboards as kb

router = Router()

#@router.message(CommandStart())
#async def cmd_start(message: Message):
   #await message.answer(f"Привіт, користувачу {message.from_user.username} 👋\nЯ — бот з розкладом ФІТ 🏫\nБудь-ласка зареєструйся у вебдодатку 🌐\n",)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.delete()
    await message.answer("Привіт, студенте [ім’я!] 👋\nЯ — бот з розкладом ФІТ 🏫\nОбери дію нижче⬇️\n")
