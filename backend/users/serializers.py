from rest_framework import serializers
from users.models import User, Profile
from botapp.models import BotUser
from botapp.serializers import BotUserSerializer


class UserSerializer(serializers.ModelSerializer):
    tg_account = BotUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'tg_account']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar']
