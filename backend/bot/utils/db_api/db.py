from botapp.models import BotUser
from users.models import User
from asgiref.sync import sync_to_async
from main.models import WordCategory, Word, UserWordCategories, UserWords

@sync_to_async
def register_user(user_id: int, phone_number: str | None, first_name: str, last_name: str | None, username: str | None):
    user = BotUser.objects.filter(user_id=user_id).first()
    
    # If user exists but has no phone number, update it
    if user:
        if not user.phone_number and phone_number:
            user.phone_number = phone_number
            user.save()
        return False  # User already exists, no need to create
    
    # Create new user
    BotUser.objects.create(
        user_id=user_id,
        phone_number=phone_number,
        first_name=first_name,
        last_name=last_name,
        username=username
    )
    return True


@sync_to_async
def check_user(user_id: int):
    return BotUser.objects.filter(user_id=user_id).exists()


@sync_to_async
def get_user(user_id: int):
    return BotUser.objects.filter(user_id=user_id).first()


@sync_to_async
def get_user_by_phone(phone_number: str):
    return BotUser.objects.filter(phone_number=phone_number).first()


@sync_to_async
def get_all_word_categories():
    return WordCategory.objects.all()


@sync_to_async
def get_category_words(category_id: int):
    return Word.objects.filter(category_id=category_id).all()


@sync_to_async
def get_word_by_id(word_id: int):
    return Word.objects.filter(id=word_id).first()


@sync_to_async
def get_user_all_word_categories(user_id: int):
    bot_user = BotUser.objects.filter(user_id=user_id).first()
    print("Bot User Found:", bot_user)  # Debug

    if not bot_user:
        return None

    user = User.objects.filter(tg_account=bot_user).first()
    print("User Found:", user)  # Debug

    if not user:
        return None

    categories = list(UserWordCategories.objects.filter(user=user))
    print("Categories Found:", categories)  # Debug

    return categories


@sync_to_async
def get_user_words_by_category(user_id: int, category_id: int):
    bot_user = BotUser.objects.filter(user_id=user_id).first()
    if not bot_user:
        return None

    user = User.objects.filter(tg_account=bot_user).first()
    if user:
        return UserWords.objects.filter(user=user, category_id=category_id).all()
    
    return None
