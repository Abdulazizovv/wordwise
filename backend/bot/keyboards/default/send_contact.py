from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

send_contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)