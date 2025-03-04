from aiogram import types
from bot.loader import dp
from bot.utils.db_api import api
from bot.keyboards.inline import categories_keyboard, categories_callback, pagination_callback
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


@dp.callback_query_handler(text="categories")
async def show_categories(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_categories = api.get_bot_user_categories(user_id)
    
    if user_categories.get('detail') == "No categories found for this user":
        await call.message.edit_text("Sizda hech qanday kategoriya mavjud emas.\n"
                                  "Yangi kategoriya qo'shish uchun 'Yangi kategoriya qo'shish ➕' tugmasini bosing.", reply_markup=types.InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [
                                                types.InlineKeyboardButton(text="Yangi kategoriya qo'shish ➕", callback_data="add_category")
                                            ],
                                            [
                                                types.InlineKeyboardButton(text="Orqaga ⬅️", callback_data="back_to_main_menu")
                                          ]
                                      ]
                                  ))
        return

    if not user_categories['results']:  # Fix: Correctly check for empty categories
        await call.message.edit_text("Sizda hech qanday kategoriya mavjud emas.\n"
                                  "Yangi kategoriya qo'shish uchun 'Yangi kategoriya qo'shish ➕' tugmasini bosing.", reply_markup=types.InlineKeyboardMarkup(
                                      inline_keyboard=[
                                          [
                                                types.InlineKeyboardButton(text="Yangi kategoriya qo'shish ➕", callback_data="add_category")
                                            ],
                                            [
                                                types.InlineKeyboardButton(text="Orqaga ⬅️", callback_data="back_to_main_menu")
                                          ]
                                      ]
                                  ))
        return
    
    page = 1  # Start from page 1
    is_next = bool(user_categories.get("next"))  # Check if there is a next page

    categories_text = "\n➖➖➖➖➖➖➖➖➖➖➖➖\n".join([
        f"{idx + 1}) {category['category_detail']['name']} - {category['category_detail']['description']} "
        f"| So'zlar soni: {category['category_detail']['words_count']}"
        for idx, category in enumerate(user_categories['results'])
    ])

    categories_keyboard_markup = categories_keyboard(user_categories['results'], page, is_next)

    await call.message.edit_text(f"Sizning kategoriyalaringiz🗃:\n"
                                 f"Jami kategoriyalar: {user_categories['count']}\n\n"
                                 f"{categories_text}", reply_markup=categories_keyboard_markup)


@dp.callback_query_handler(pagination_callback.filter())
async def paginate_categories(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    current_page = int(callback_data["page"])

    user_id = call.from_user.id

    # Determine new page number based on action
    if action == "next":
        new_page = current_page + 1
    elif action == "prev":
        new_page = max(1, current_page - 1)  # Prevent negative or zero pages
    else:
        return  # If action is invalid, do nothing

    # Fetch new page of categories
    user_categories = api.get_bot_user_categories(user_id, page=new_page)

    if not user_categories['results']:  # Fix: Correctly check for empty results
        await call.answer("Hech qanday kategoriya topilmadi.", show_alert=True)
        return

    is_next = bool(user_categories.get("next"))  # Check if there is a next page

    categories_text = "\n➖➖➖➖➖➖➖➖➖➖➖➖\n".join([
        f"{idx + 1}) {category['category_detail']['name']} - {category['category_detail']['description']} "
        f"| So'zlar soni: {category['category_detail']['words_count']}"
        for idx, category in enumerate(user_categories['results'], start=(new_page - 1) * 5)
    ])

    categories_keyboard_markup = categories_keyboard(user_categories['results'], new_page, is_next)

    await call.message.edit_text(f"Sizning kategoriyalaringiz🗃:\n"
                                 f"Jami kategoriyalar: {user_categories['count']} ta\n\n"
                                 f"{categories_text}", reply_markup=categories_keyboard_markup)


@dp.message_handler(Command("new_category"))
async def new_category(message: types.Message, state: FSMContext):
    # Fix: Reset state before starting new state
    await state.finish()

    await message.answer("Kategoriya nomini kiriting:")
    await state.set_state("category_name")



@dp.callback_query_handler(text="add_category")
async def add_category(call: types.CallbackQuery, state: FSMContext):
    # Fix: Reset state before starting new state
    await state.finish()

    # Start new state
    await call.message.edit_text("Kategoriya nomini kiriting:")
    await state.set_state("category_name")


@dp.message_handler(state="category_name")
async def add_category_name(message: types.Message, state: FSMContext):
    # Check if category name is not exist
    user_id = message.from_user.id
    category_name = message.text

    response = api.check_category_exists(category_name, user_id)

    if response.get('detail') == "Exists":
        await message.answer("⚠️ Bu nomdagi kategoriya allaqachon mavjud. Boshqa nom kiriting.")
        return

    # Save category text in state
    await state.update_data(category_name=message.text)
    
    # Start new state
    await message.answer("Kategoriyaning tavsifini kiriting:")
    await state.set_state("category_description")


@dp.message_handler(state="category_description")
async def add_category_description(message: types.Message, state: FSMContext):
    
    # Get data from state
    data = await state.get_data()
    user_id = message.from_user.id

    # get category name and description from state
    category_name = data["category_name"]
    category_description = message.text

    # Create category in database using API
    response = api.create_category(user_id, category_name, category_description)

    if response.get('detail') == "OK":
        await message.answer("✅ Kategoriya muvaffaqqiyatli yaratildi!")
    elif response.get('detail') == "Exists":
        await message.answer("⚠️ Bu nomdagi kategoriya allaqachon mavjud.")
    else:
        await message.answer("❌ Kategoriyani yaratishda xatolik yuz berdi.")

    await state.finish()


@dp.callback_query_handler(categories_callback.filter())
async def show_category(call: types.CallbackQuery, callback_data: dict):
    category_id = int(callback_data["id"])
    await call.message.edit_text(f"Kategoriya: {category_id}")
