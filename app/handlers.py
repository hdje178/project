from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import dialog_calendar, simple_calendar, simple_cal_callback, dialog_cal_callback, SimpleCalendar
import datetime
from config import WEEK_DAYS

import app.keyboards as kb

class ScheduleStates(StatesGroup):
    current_date = State()  

router = Router()
selected_dates = {}
register_user = {1486454337}

def is_user_registered(user_id: int) -> bool:
    return int(user_id) in register_user

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

@router.callback_query(F.data == "timetable_for_day")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"📅 Розклад на день {datetime.date.today()} :\n [Якийсь розклад]", reply_markup= kb.table_one)

@router.callback_query(F.data == "back_to_main")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Привіт, студенте [ім’я!] 👋\nЯ — бот з розкладом ФІТ 🏫\nОбери дію нижче⬇️\n", reply_markup= kb.main)


@router.callback_query(F.data == "alert_settings")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("⚙️ Налаштування повідомлень відбувається в web app \n", reply_markup= kb.alert_setting)

@router.callback_query(F.data == "timetable_for_next_day")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f"🗓️ Розклад на завтра {datetime.date.today()+datetime.timedelta(days=1)} :\n [Якийсь розклад]", reply_markup= kb.back_keyboard)    


#@router.callback_query(F.data == "open_calendar")
#async def open_calendar(callback: CallbackQuery):
   # await callback.answer()  
   #reply_markup = await UkrainianCalendar().start_calendar()
 #   await callback.message.edit_text(
 #      ,
 #       reply_markup=reply_markup
 #   )
@router.callback_query(F.data == "timetable_for_day_you_want")
async def catalog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ScheduleStates.current_date)

    cal_markup = await SimpleCalendar().start_calendar()
    exit_btn = InlineKeyboardButton(text="Вийти ❌", callback_data="calendar_exit")
    cal_markup.inline_keyboard.append([exit_btn])
    reply_markup = cal_markup


    await callback.message.edit_text(
        "🗓️ Оберіть день:\n ",
        reply_markup=reply_markup
    )

@router.callback_query(simple_cal_callback.filter())
async def process_calendar(callback: CallbackQuery, callback_data: dict, state: FSMContext):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback, callback_data)

    if not selected:
        return

    current_state = await state.get_state()
    if current_state != ScheduleStates.current_date:
        return


    await state.update_data(current_day=date.strftime('%Y-%m-%d'))


    await callback.message.edit_text(
        f"🗓️ Розклад на {date.strftime('%Y-%m-%d')}:\n[Якийсь розклад]",
        reply_markup=kb.back_keyboard
    )
    await state.clear()  


@router.callback_query(F.data == "calendar_exit")
async def cancel_calendar(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("Вибір дати скасовано.", reply_markup=kb.main)
     

def get_monday(d: datetime.date) -> datetime.date:
    return d - datetime.timedelta(days=d.weekday())

@router.callback_query(F.data == "timetable_for_week")
async def catalog(callback: CallbackQuery):
    await callback.answer()

    start_date = get_monday(datetime.date.today())              
    end_date = start_date + datetime.timedelta(days=6)       

    await callback.message.edit_text(
        f"🗓️ Розклад на тиждень {start_date.strftime('%d.%m.%y')} - {end_date.strftime('%d.%m.%y')}:\n[Якийсь розклад]",
        reply_markup= kb.table_two
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


