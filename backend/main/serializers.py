from rest_framework import serializers
from .models import Word, WordCategory, Question, UserWordCategories, UserWords, UserQuestions
from users.serializers import UserSerializer
from users.models import User

class WordCategorySerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="owner", write_only=True
    )
    owner = UserSerializer(read_only=True)
    class Meta:
        model = WordCategory
        fields = '__all__'



class WordSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=WordCategory.objects.all(), source="category", write_only=True
    )
    category = WordCategorySerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="owner", write_only=True
    )
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Word
        fields = '__all__'