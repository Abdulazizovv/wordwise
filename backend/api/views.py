from rest_framework import viewsets
from botapp.models import BotUser
from main.models import Word, WordCategory, Question, UserWordCategories, UserWords, UserQuestions

from botapp.serializers import BotUserSerializer


class BotUserViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
