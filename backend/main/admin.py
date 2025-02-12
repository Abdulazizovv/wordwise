from django.contrib import admin
from .models import WordCategory, Word, Question, Option, Answer


class WordInline(admin.TabularInline):  # Inline for Words inside WordCategory
    model = Word
    extra = 1
    fields = ('name', 'description', 'type', 'owner', 'created_at')
    readonly_fields = ('created_at',)


class QuestionInline(admin.TabularInline):  # Inline for Questions inside Word
    model = Question
    extra = 1
    fields = ('text', 'owner', 'created_at')
    readonly_fields = ('created_at',)


class OptionInline(admin.TabularInline):  # Inline for Options inside Question
    model = Option
    extra = 2
    fields = ('name', 'is_correct', 'owner', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(WordCategory)
class WordCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'type', 'get_words_count', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('type', 'created_at')
    inlines = [WordInline]  # Display words inside category page

    def get_words_count(self, obj):
        return obj.words.count()
    get_words_count.short_description = 'Word Count'


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'type', 'owner', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'type', 'created_at')
    inlines = [QuestionInline]  # Display questions inside word page


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'word', 'owner', 'created_at')
    search_fields = ('text', 'word__name')
    list_filter = ('created_at',)
    inlines = [OptionInline]  # Display options inside question page


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'question', 'is_correct', 'owner', 'created_at')
    search_fields = ('name', 'question__text')
    list_filter = ('is_correct', 'created_at')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'option', 'owner', 'created_at')
    search_fields = ('question__text', 'option__name')
    list_filter = ('created_at',)
