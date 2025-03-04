from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

categories_callback = CallbackData("category", "id")
pagination_callback = CallbackData("pagination", "action", "page")

def categories_keyboard(categories, page: int = 1, is_next: bool = False):
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    # Display category names instead of just numbers
    for category in categories:
        keyboard.add(InlineKeyboardButton(
            text=category["category_detail"]["name"],  # Show category name
            callback_data=categories_callback.new(id=category["id"])
        ))
    
    # Pagination buttons
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi", callback_data=pagination_callback.new(action="prev", page=page)
        ))
    if is_next:
        pagination_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️", callback_data=pagination_callback.new(action="next", page=page)
        ))
    
    if pagination_buttons:
        keyboard.row(*pagination_buttons)
    
    # Add category creation button
    keyboard.add(InlineKeyboardButton(text="Yangi kategoriya qo'shish ➕", callback_data="add_category"))
    # Add back button
    keyboard.add(InlineKeyboardButton(text="Orqaga ⬅️", callback_data="back_to_main_menu"))
    
    return keyboard
