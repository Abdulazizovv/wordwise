from django.contrib import admin
from .models import (
    WordCategory, Word, Question, Option, Answer,
    UserWords, UserWordCategories, UserQuestions
)

@admin.register(WordCategory)
class WordCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('type', 'created_at')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'type', 'owner', 'created_at')
    search_fields = ('name', 'category__name', 'owner__username')
    list_filter = ('type', 'created_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'word', 'owner', 'created_at')
    search_fields = ('text', 'word__name', 'owner__username')
    list_filter = ('created_at',)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'question', 'is_correct', 'owner', 'created_at')
    search_fields = ('name', 'question__text', 'owner__username')
    list_filter = ('is_correct', 'created_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'option', 'owner', 'created_at')
    search_fields = ('question__text', 'option__name', 'owner__username')
    list_filter = ('created_at',)

@admin.register(UserWords)
class UserWordsAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'category', 'is_favorite', 'is_learned', 'created_at')
    search_fields = ('user__username', 'word__name', 'category__name')
    list_filter = ('is_favorite', 'is_learned', 'created_at')

@admin.register(UserWordCategories)
class UserWordCategoriesAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'is_favorite', 'is_learned', 'created_at')
    search_fields = ('user__username', 'category__name')
    list_filter = ('is_favorite', 'is_learned', 'created_at')

@admin.register(UserQuestions)
class UserQuestionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_favorite', 'is_learned', 'created_at')
    search_fields = ('user__username', 'question__text')
    list_filter = ('is_favorite', 'is_learned', 'created_at')
