from aiogram import types
from bot.loader import dp


@dp.callback_query_handler(text="categories")
async def show_categories(call: types.CallbackQuery):
    pass