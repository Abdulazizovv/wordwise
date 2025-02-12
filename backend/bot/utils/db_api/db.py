from botapp.models import BotUser
from asgiref.sync import sync_to_async


@sync_to_async
def register_user(user_id: int, phone_number: str|None, first_name: str, last_name: str|None, username: str|None):
    # check if user already exists
    user = BotUser.objects.filter(user_id=user_id).first()
    if user and not user.phone_number:
        return False
    if user and user.phone_number and phone_number:
        user.phone_number = phone_number
        user.save()
        return False
    # create new user
    user = BotUser.objects.create(user_id=user_id, phone_number=phone_number, first_name=first_name, last_name=last_name, username=username)
    return True


@sync_to_async
def check_user(user_id: int):
    return BotUser.objects.filter(user_id=user_id).exists()