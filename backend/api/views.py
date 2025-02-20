from rest_framework import viewsets
from botapp.models import BotUser
from main.models import Word, WordCategory, Question, UserWordCategories, UserWords, UserQuestions
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from botapp.serializers import BotUserSerializer
from main.serializers import WordSerializer, WordCategorySerializer, UserWordCategoriesSerializer
from users.serializers import UserSerializer
from users.models import User
from django.shortcuts import get_object_or_404
import logging


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'tg_account'


class BotUserViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    lookup_field = 'user_id'

    @action(detail=False, methods=['get'])
    def check_user(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"detail: user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = BotUser.objects.filter(user_id=user_id).first()

        return Response({True}, status=status.HTTP_200_OK) if user else Response({False}, status=status.HTTP_200_OK)


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class WordCategoryViewSet(viewsets.ModelViewSet):
    queryset = WordCategory.objects.all()
    serializer_class = WordCategorySerializer

    @action(detail=False, methods=['post'])
    def create_category(self, request):
        user_id = request.data.get('user_id')
        category_name = request.data.get('category_name')
        category_description = request.data.get('category_description')

        if not user_id or not category_name or not category_description:
            return Response({"detail": "user_id, category_name and category_description are required"}, status=status.HTTP_400_BAD_REQUEST)

        tg_account = get_object_or_404(BotUser, user_id=user_id)
        user = get_object_or_404(User, tg_account=tg_account)
        
        if WordCategory.objects.filter(name=category_name).exists():
            return Response({"detail": "Exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            WordCategory.objects.create(name=category_name, description=category_description, owner=user)
        except Exception as err:
            logging.error(err)
            return Response({"detail": "Error"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "OK"}, status=status.HTTP_201_CREATED)


class UserWordCategoriesViewSet(viewsets.ModelViewSet):
    queryset = UserWordCategories.objects.all()
    serializer_class = UserWordCategoriesSerializer

    @action(detail=False, methods=['get'])
    def get_bot_user_categories(self, request):
        user_id = request.query_params.get('user_id')  # Get user_id from query params
        if not user_id:
            return Response({"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        bot_user = get_object_or_404(BotUser, user_id=user_id)
        user = get_object_or_404(User, tg_account=bot_user)

        user_categories = UserWordCategories.objects.filter(user=user)
        if not user_categories.exists():
            return Response({"detail": "No categories found for this user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserWordCategoriesSerializer(user_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    