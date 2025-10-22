from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import dialog_calendar, simple_calendar, simple_cal_callback, dialog_cal_callback, SimpleCalendar
from datetime import datetime, date, timedelta

from app.keyboards import keyboard_back_to_day_menu, keyboard_back_to_week_menu
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

# --- Короткий розклад для тижня ---
def short_day_schedule(day: date) -> str:
    days_uk = {
        0: "Понеділок",
        1: "Вівторок",
        2: "Середа",
        3: "Четвер",
        4: "Пʼятниця",
        5: "Субота",
        6: "Неділя"
    }
    day_name = days_uk[day.weekday()]
    return (f"<b>{day_name} {day.strftime('%d.%m')}</b>\n"
            f"<b>1 пара</b> Алгебра\n"
            f"<b>2 пара</b> Фізика\n"
            f"<b>3 пара</b> Програмування\n\n")

# --- Розклад на тиждень ---
async def show_schedule_for_week(message_or_callback, monday: date):
    text = "🗓️ <b>Розклад на тиждень:</b>\n\n"
    for i in range(5):
        text += short_day_schedule(monday + timedelta(days=i))
    text += "📚 Успішного тижня!"

    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.message.edit_text(text=text, reply_markup=keyboard_back_to_week_menu, parse_mode="HTML")
    else:
        await message_or_callback.answer(text=text, reply_markup=keyboard_back_to_week_menu, parse_mode="HTML")


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

#---Головне меню---
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Привіт, студенте [ім’я!] 👋\n"
        "Я — бот з розкладом ФІТ 🏫\n"
        "Обери дію нижче⬇️\n",
        reply_markup= kb.main)

#---Меню налаштувань повідомлень---
@router.callback_query(F.data == "alert_settings")
async def alert_settings(callback: CallbackQuery):
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


    # Повертаємо обрану дату# --- обробка усіх натискань у календарі ---
@router.callback_query(simple_cal_callback.filter())
async def process_calendar(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback, callback_data)

    if not selected:
        # Якщо користувач просто перемикає місяць або рік —
        # календар оновився → додаємо кнопку "Вийти ❌" знову
        markup = callback.message.reply_markup
        exit_btn = InlineKeyboardButton(text="Вийти ❌", callback_data="calendar_exit")

        # якщо кнопки немає — додаємо
        if all(btn.text != "Вийти ❌" for row in markup.inline_keyboard for btn in row):
            markup.inline_keyboard.append([exit_btn])

        await callback.message.edit_reply_markup(reply_markup=markup)
        return

    # Якщо користувач обрав дату
    current_state = await state.get_state()
    if current_state != ScheduleStates.current_date:
        return

    await state.update_data(current_day=date.strftime('%d.%m.%Y'))
    await state.clear()
    #await callback.message.delete()
    await show_schedule_for_date(callback, date)

#---Повертає початок тижня для любої дати---
def get_monday(d: datetime.date) -> datetime.date:
    return d - timedelta(days=d.weekday())

#---Меню вибору на який тиждень розклад---
@router.callback_query(F.data == "timetable_for_week")
async def catalog(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "🗓️ <b>Розклад на тиждень</b>\nОбери дію нижче ⬇️",
        reply_markup= kb.keyboard_week,
        parse_mode="HTML"
    )

# --- Обробка кнопок тижня ---
@router.callback_query(F.data.in_({"timetable_for_that_week", "timetable_for_next_week"}))
async def show_week_schedule_callback(callback: CallbackQuery):
    monday = get_monday(date.today())
    if callback.data == "timetable_for_next_week":
        monday += timedelta(days=7)
    await show_schedule_for_week(callback, monday)



