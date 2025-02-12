from django.db import models

class WordCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey('users.User', related_name='word_categories', on_delete=models.CASCADE, null=True, blank=True)
    
    TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='private')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_words_count(self):
        return self.words.count()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Word Categories'


class Word(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(WordCategory, related_name='words', on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', related_name='words', on_delete=models.CASCADE, null=True, blank=True)
    
    TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='private')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Words'


class Question(models.Model):
    text = models.TextField(blank=False)  # Ensure questions cannot be empty
    word = models.ForeignKey(Word, related_name='questions', on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', related_name='questions', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text or f"Question for {self.word.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Questions'


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    owner = models.ForeignKey('users.User', related_name='options', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Correct: {self.is_correct})"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Options'


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='answers', on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', related_name='answers', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to '{self.question.text}': {self.option.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Answers'


class UserWords(models.Model):
    user = models.ForeignKey('users.User', related_name='user_words', on_delete=models.CASCADE)
    word = models.ForeignKey(Word, related_name='user_words', on_delete=models.CASCADE)
    category = models.ForeignKey(WordCategory, related_name='user_words', on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    is_learned = models.BooleanField(default=False)
    is_difficult = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    is_ignored = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.word.name} ({self.category.name})"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Words'
        unique_together = ('user', 'word', 'category')


class UserWordCategories(models.Model):
    user = models.ForeignKey('users.User', related_name='user_word_categories', on_delete=models.CASCADE)
    category = models.ForeignKey(WordCategory, related_name='user_word_categories', on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    is_learned = models.BooleanField(default=False)
    is_difficult = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    is_ignored = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Word Categories'
        unique_together = ('user', 'category')


class UserQuestions(models.Model):
    user = models.ForeignKey('users.User', related_name='user_questions', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='user_questions', on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    is_learned = models.BooleanField(default=False)
    is_difficult = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    is_ignored = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question.text}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Questions'
        unique_together = ('user', 'question')
