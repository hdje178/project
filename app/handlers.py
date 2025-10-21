from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import dialog_calendar, simple_calendar, simple_cal_callback, dialog_cal_callback, SimpleCalendar
from datetime import datetime, date, timedelta

from app.keyboards import keyboard_back_to_day_menu
from config import WEEK_DAYS

import app.keyboards as kb

class ScheduleStates(StatesGroup):
    current_date = State()  

router = Router()
selected_dates = {}
register_user = {1486454337}


def is_user_registered(user_id: int) -> bool:
    return int(user_id) in register_user

# --- Розклад на день ---
async def show_schedule_for_date(message_or_callback, day: date):
    text = (
        f"📘 <b>Розклад на {day.strftime('%d.%m.%Y')}:</b>\n\n"
        f"Номер пари\n"
        f"🎓 Назва пари\n"
        f"🕒 Час: 09:00–10:20\n"
        f"👨‍🏫 Викладач: Ім’я Прізвище\n"
        f"📍 Аудиторія №123 \ Посилання htpps\...\n"
    )

    # Перевіряємо, чи об'єкт є CallbackQuery (натискання inline-кнопки)
    # Якщо так — редагуємо текст вже існуючого повідомлення та оновлюємо клавіатуру
    # Інакше (Message) — надсилаємо нове повідомлення з текстом та клавіатурою
    # parse_mode="HTML" дозволяє використовувати HTML-теги у тексті
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(text=text, reply_markup=keyboard_back_to_day_menu, parse_mode="HTML")
    else:
        await message_or_callback.answer(text=text, reply_markup=keyboard_back_to_day_menu, parse_mode="HTML")

# --- Хендлер для /start
@router.message(CommandStart())
async def cmd_start(message: Message):
   # user_id = message.from_user.id

    #if not is_user_registered(user_id):
       # await message.answer(
          #  f"Привіт, користувачу {message.from_user.username or ""} 👋\n"
          #  "Будь-ласка зареєструйся у вебдодатку 🌐\n"
       # )
     #   return


 #   await message.delete()
    await message.answer(
       f"Привіт, студенте [ім’я!] 👋\nЯ — бот з розкладом ФІТ 🏫\nОбери дію нижче⬇️\n",
        reply_markup=kb.main
    )

#---Меню для вибору дня---
@router.callback_query(F.data == "timetable_for_day")
async def day_schedule_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text="📅 <b>Розклад на день</b>\nОбери дію нижче ⬇️",
        reply_markup=kb.keyboard_day,
        parse_mode="HTML"
    )

#---Хендлер для розкладу на сьогодні/завтра---
@router.callback_query(F.data.in_({"timetable_for_today", "timetable_for_tomorrow"}))
async def day_schedule_callback(callback: CallbackQuery):
    day = date.today() if callback.data == "timetable_for_today" else date.today() + timedelta(days=1)
    await show_schedule_for_date(callback, day)

@router.callback_query(F.data == "back_to_main")
async def get_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Привіт, студенте [ім’я!] 👋\nЯ — бот з розкладом ФІТ 🏫\nОбери дію нижче⬇️\n", reply_markup= kb.main)


@router.callback_query(F.data == "alert_settings")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "⚙️ Налаштування повідомлень відбувається в web app \n", reply_markup= kb.alert_setting)


#@router.callback_query(F.data == "open_calendar")
#async def open_calendar(callback: CallbackQuery):
   # await callback.answer()  
   #reply_markup = await UkrainianCalendar().start_calendar()
 #   await callback.message.edit_text(
 #      ,
 #       reply_markup=reply_markup
 #   )

#---Виводить календар та запитує день у користувача---
@router.callback_query(F.data == "timetable_for_day_you_want")
async def ask_for_day(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ScheduleStates.current_date)

    cal_markup = await SimpleCalendar().start_calendar()
    exit_btn = InlineKeyboardButton(text="Вийти ❌", callback_data="timetable_for_day")
    cal_markup.inline_keyboard.append([exit_btn])
    reply_markup = cal_markup

    await callback.message.edit_text(
        "🗓️ Оберіть день:\n ",
        reply_markup=reply_markup
    )

#---Обробляє натискання кнопок календаря, зберігає обрану дату і передає її у функцію---
@router.callback_query(simple_cal_callback.filter())
async def process_calendar(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback, callback_data)

    if not selected:
        # Дата ще не остаточно вибрана
        return None

    # Перевіряємо стан FSM — чи бот очікує вибір дати
    current_state = await state.get_state()
    if current_state != ScheduleStates.current_date:
        return None

    # Зберігаємо обрану дату у стані
    await state.update_data(current_day=date.strftime('%d.%m.%Y'))

    # Очищаємо стан
    await state.clear()

    # Повертаємо обрану дату
    await show_schedule_for_date(callback.message, date)

def get_monday(d: datetime.date) -> datetime.date:
    return d - datetime.timedelta(days=d.weekday())

@router.callback_query(F.data == "timetable_for_week")
async def catalog(callback: CallbackQuery):
    await callback.answer()

    start_date = get_monday(datetime.date.today())              
    end_date = start_date + datetime.timedelta(days=6)       

    await callback.message.edit_text(
        "📘 Виберіть на який тиждень :\n", reply_markup= kb.table_two
    )

@router.callback_query(F.data == "timetable_for_next_week")
async def catalog(callback: CallbackQuery):
    await callback.answer()

    start_date = get_monday(datetime.date.today()) + datetime.timedelta(days=7)  
    end_date = start_date + datetime.timedelta(days=6)                    

    await callback.message.edit_text(
        f"🗓️ Розклад на тиждень {start_date.strftime('%d.%m.%y')} - {end_date.strftime('%d.%m.%y')}:\n[Якийсь розклад]",
        reply_markup= kb.table_two
    )

@router.callback_query(F.data == "timetable_for_that_week")
async def catalog(callback: CallbackQuery):
    await callback.answer()  
    start_date = get_monday(datetime.date.today())              
    end_date = start_date + datetime.timedelta(days=6)                  

    await callback.message.edit_text(
        f"🗓️ Розклад на тиждень {start_date.strftime('%d.%m.%y')} - {end_date.strftime('%d.%m.%y')}:\n\n",
        reply_markup= kb.table_two
    )


