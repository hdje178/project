from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

BACK = "◀️ Назад"

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Розклад на день", callback_data="timetable_for_day")],
    [InlineKeyboardButton(text="🗓️ Розклад на тиждень", callback_data="timetable_for_week"),
      InlineKeyboardButton(text="⚙️ Налаштування сповіщень", callback_data= "alert_settings")]
])
table_one = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Розклад на завтра", callback_data="timetable_for_next_day")],
    [InlineKeyboardButton(text="📅 Вибрати день самостійно", callback_data="timetable_for_day_you_want"),
      InlineKeyboardButton(text=BACK, callback_data="back_to_main")]
])
table_two = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📘 Цей тиждень", callback_data="timetable_for_week")],
    [InlineKeyboardButton(text="📗 Наступний тиждень", callback_data="timetable_for_next_week"),
      InlineKeyboardButton(text=BACK, callback_data="back_to_main")]
])
alert_setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=BACK, callback_data="back_to_main"),
    InlineKeyboardButton(text="Відкрити web app", callback_data="web_app")]
])

back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])