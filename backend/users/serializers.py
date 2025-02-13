from .models import User
from rest_framework import serializers
from botapp.models import BotUser
from botapp.serializers import BotUserSerializer

class UserSerializer(serializers.ModelSerializer):
    tg_account = BotUserSerializer(read_only=True)
    tg_account_id = serializers.PrimaryKeyRelatedField(
        queryset=BotUser.objects.all(), source="tg_account", write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'is_active', 'tg_account', 'tg_account_id', 'date_joined', 'last_login')