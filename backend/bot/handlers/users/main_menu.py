from aiogram import types
from bot.loader import dp
from bot.keyboards.inline import main_menu_kb


@dp.callback_query_handler(text="back_to_main_menu")
async def back_to_main_menu(call: types.CallbackQuery):
    await call.message.edit_text("Asosiy menyu", reply_markup=main_menu_kb)