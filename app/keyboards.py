from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Розклад на день", callback_data="timetable_for_day")],
    [InlineKeyboardButton(text="🗓️ Розклад на тиждень", callback_data="timetable_for_week"),
      InlineKeyboardButton(text="⚙️ Налаштування сповіщень", callback_data= "allert_settings")]
])
table_one = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Розклад на cьогодні", callback_data="timetable_for_today"),
     InlineKeyboardButton(text="📅 Розклад на наступний день", callback_data="timetable_for_next_day")],
    [InlineKeyboardButton(text="📅 Вибрати день самостійно", callback_data="timetable_for_day_you_want"),
      InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
])
table_two = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📘 Цей тиждень", callback_data="timetable_for_week")],
    [InlineKeyboardButton(text="📗 Наступний тиждень", callback_data="timetable_for_next_week"),
      InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
])
