from rest_framework import viewsets
from botapp.models import BotUser
from main.models import Word, WordCategory, Question, UserWordCategories, UserWords, UserQuestions
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from botapp.serializers import BotUserSerializer


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