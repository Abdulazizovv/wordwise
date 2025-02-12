from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
from bot.utils.db_api.db import register_user, check_user
from aiogram.dispatcher import FSMContext
from bot.keyboards.default import send_contact_kb


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    user_exists = await check_user(message.from_user.id)
    if not user_exists:
        await message.answer("Assalomu alaykum!\n"\
                             "WordWise botiga xush kelibsiz😇\n"\
                             "Ro\'yxatdan o'tish uchun iltimos telefon raqamingizni yuboring\n\n"\
                             "Pastdagi tugmani bosing👇", reply_markup=send_contact_kb)
        await state.set_state("phone_number")
    else:
        await message.answer("Siz avval ro'yxatdan o'tgansiz!")
        await state.finish()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state="phone_number")
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await register_user(message.from_user.id, phone_number, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    await message.answer("Rahmat! Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
    await state.finish()



