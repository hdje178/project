from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

BACK = "↩️ Назад"

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Розклад на день", callback_data="timetable_for_day")],
    [InlineKeyboardButton(text="🗓️ Розклад на тиждень", callback_data="timetable_for_week")],
    [InlineKeyboardButton(text="⚙️ Налаштування сповіщень", callback_data= "alert_settings")]
])

keyboard_day = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💼 На сьогодні", callback_data="timetable_for_today")],
    [InlineKeyboardButton(text="🌅 На завтра", callback_data="timetable_for_tomorrow")],
    [InlineKeyboardButton(text="🗓️ На інший день", callback_data="timetable_for_day_you_want")],
    [InlineKeyboardButton(text=BACK, callback_data="back_to_main")]
])

keyboard_back_to_day_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="↩️ Назад", callback_data="timetable_for_day")],
    [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
])

keyboard_back_to_week_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="↩️ Назад", callback_data="timetable_for_week")],
    [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
])

keyboard_week = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📘 Цей тиждень", callback_data="timetable_for_that_week")],
    [InlineKeyboardButton(text="📗 Наступний тиждень", callback_data="timetable_for_next_week")],
    [InlineKeyboardButton(text=BACK, callback_data="back_to_main")]
])

alert_setting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀Відкрити вебзастосунок", web_app=WebAppInfo(url="https://google.com"))],
    [InlineKeyboardButton(text=BACK, callback_data="back_to_main")]
])




