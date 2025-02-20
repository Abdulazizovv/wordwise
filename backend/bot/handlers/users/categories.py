from aiogram import types
from bot.loader import dp
from bot.utils.db_api import api
from bot.keyboards.inline import categories_keyboard, categories_callback
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="categories")
async def show_categories(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_categories = api.get_bot_user_categories(user_id)
    if not user_categories:
        await call.message.answer("You don't have any categories yet")
        return
    
    categories = "\n".join([f"{idx+1}) {category['category_detail']['name']} - {category['category_detail']['description']} |So'zlar soni: {category['category_detail']['words_count']}" for idx, category in enumerate(user_categories)])
    await call.message.answer(f"Sizning kategoriyalaringiz🗃:\n{categories}", reply_markup=categories_keyboard(user_categories))


@dp.callback_query_handler(text="add_category")
async def add_category(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Kategoriya nomini kiriting")
    await state.set_state("category_name")


@dp.message_handler(state="category_name")
async def add_category_name(message: types.Message, state: FSMContext):
    category_name = message.text
    await state.update_data(category_name=category_name)
    await message.answer("Kategoriyani tavsifini kiriting")
    await state.set_state("category_description")


@dp.message_handler(state="category_description")
async def add_category_description(message: types.Message, state: FSMContext):
    category_description = message.text
    await state.update_data(category_description=category_description)
    data = await state.get_data()
    user_id = message.from_user.id
    category_name = data.get("category_name")
    category_description = data.get("category_description")
    response = api.create_category(user_id, category_name, category_description)
    if response['detail'] == "OK":
        await message.answer("Kategoriya muvaffaqqiyatli yaratildi✅")
    elif response['detail'] == "Exists":
        await message.answer("Bu nomdagi kategoriya mavjud❌")
    else:
        await message.answer("Kategoriyani yaratishda xatolik yuz berdi❌")
    await state.finish()


@dp.callback_query_handler(categories_callback.filter())
async def show_category(call: types.CallbackQuery, callback_data: dict):
    category_id = int(callback_data.get("id"))
    await call.message.answer(f"Category {category_id}")


