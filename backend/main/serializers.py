from rest_framework import serializers
from main.models import WordCategory, Word, Question, Option, Answer, UserWords, UserWordCategories, UserQuestions
from users.models import User
from users.serializers import UserSerializer


class WordCategorySerializer(serializers.ModelSerializer):
    owner_detail = UserSerializer(source='owner', read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    words_count = serializers.IntegerField(source='get_words_count', read_only=True)

    class Meta:
        model = WordCategory
        fields = ['id', 'name', 'description', 'type', 'owner', 'owner_detail','words_count']


class WordSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    owner_detail = UserSerializer(source='owner', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=WordCategory.objects.all(), write_only=True)
    category_detail = WordCategorySerializer(source='category', read_only=True)

    class Meta:
        model = Word
        fields = ['id', 'name', 'translation', 'description', 'category', 'owner', 'owner_detail', 'category_detail']


class QuestionSerializer(serializers.ModelSerializer):
    word = serializers.PrimaryKeyRelatedField(queryset=Word.objects.all(), write_only=True)
    word_detail = WordSerializer(source='word', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'word', 'word_detail']


class OptionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True)
    question_detail = QuestionSerializer(source='question', read_only=True)

    class Meta:
        model = Option
        fields = ['id', 'name', 'is_correct', 'question', 'question_detail']


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True)
    option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all(), write_only=True)
    question_detail = QuestionSerializer(source='question', read_only=True)
    option_detail = OptionSerializer(source='option', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'option', 'question_detail', 'option_detail']


class UserWordsSerializer(serializers.ModelSerializer):
    word = serializers.PrimaryKeyRelatedField(queryset=Word.objects.all(), write_only=True)
    word_detail = WordSerializer(source='word', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=WordCategory.objects.all(), write_only=True)
    category_detail = WordCategorySerializer(source='category', read_only=True)

    class Meta:
        model = UserWords
        fields = ['id', 'user', 'word', 'category', 'word_detail', 'category_detail', 'is_favorite', 'is_learned', 'is_difficult']


class UserWordCategoriesSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=WordCategory.objects.all(), write_only=True)
    category_detail = WordCategorySerializer(source='category', read_only=True)

    class Meta:
        model = UserWordCategories
        fields = ['id', 'user', 'category', 'category_detail', 'is_favorite', 'is_learned', 'is_difficult']


class UserQuestionsSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True)
    question_detail = QuestionSerializer(source='question', read_only=True)

    class Meta:
        model = UserQuestions
        fields = ['id', 'user', 'question', 'question_detail', 'is_favorite', 'is_learned', 'is_difficult']
