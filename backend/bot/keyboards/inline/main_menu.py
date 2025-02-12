from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🗃 Kategoriyalar", callback_data="categories"),
            InlineKeyboardButton(text="📚 So'zlar", callback_data="words")
        ],
        [
            InlineKeyboardButton(text="📊 Natijalar", callback_data="results")
        ],
        [
            InlineKeyboardButton(text="🔧 Sozlamalar", callback_data="settings")
        ]
    ]
)