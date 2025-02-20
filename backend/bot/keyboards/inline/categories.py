from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

categories_callback = CallbackData("category", "id")

def categories_keyboard(categories):

    keyboard = InlineKeyboardMarkup(row_width=1)
    for idx, category in enumerate(categories):
        keyboard.add(InlineKeyboardButton(text=str(idx+1), callback_data=categories_callback.new(id=category["id"])))

    keyboard.add(InlineKeyboardButton(text="Yangi kategoriya qo'shish", callback_data="add_category"))

    return keyboard