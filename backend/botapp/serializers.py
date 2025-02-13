from .models import BotUser
from rest_framework import serializers


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ['id', 'user_id', 'phone_number', 'first_name', 'last_name', 'username', 'language_code']

