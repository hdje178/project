from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram3_calendar import dialog_calendar, simple_calendar, simple_cal_callback, dialog_cal_callback, SimpleCalendar

import app.keyboards as kb

class ScheduleStates(StatesGroup):
    current_date = State()  

router = Router()

#@router.message(CommandStart())
#async def cmd_start(message: Message):
   #await message.answer(f"Привіт, користувачу {message.from_user.username} 👋\nЯ — бот з розкладом ФІТ 🏫\nБудь-ласка зареєструйся у вебдодатку 🌐\n",)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.delete()
    await message.answer("Привіт, студенте [ім’я!] 👋\nЯ — бот з розкладом ФІТ 🏫\nОбери дію нижче⬇️\n", reply_markup=kb.main)

@router.callback_query(F.data == "timetable_for_day")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("📅 Розклад на день:\n [Якийсь розклад]", reply_markup= kb.table_one)

@router.callback_query(F.data == "back_to_main")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Привіт, студенте [ім’я!] 👋\nЯ — бот з розкладом ФІТ 🏫\nОбери дію нижче⬇️\n", reply_markup= kb.main)

@router.callback_query(F.data == "timetable_for_week")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("📅 Розклад на тиждень:\n [Якийсь розклад]", reply_markup= kb.table_two)

@router.callback_query(F.data == "alert_settings")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("⚙️ Налаштування повідомлень відбувається в web app \n", reply_markup= kb.alert_setting)

@router.callback_query(F.data == "timetable_for_next_day")
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("🗓️ Розклад на завтра:\n [Якийсь розклад]", reply_markup= kb.back_keyboard)    


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
    await callback.message.edit_text(
        "🗓️ Оберіть день:\n ",
        reply_markup=await SimpleCalendar().start_calendar()
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
     