from .models import BotUser
from rest_framework import serializers


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = '__all__'
    

