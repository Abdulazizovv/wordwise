from .models import WordCategory, Word, Question, Option, Answer, UserWords, UserWordCategories, UserQuestions
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.db.models.signals import pre_delete

@receiver(post_save, sender=WordCategory)
def create_user_word_category(sender, instance, created, **kwargs):
    if created:
        UserWordCategories.objects.create(user=instance.owner, category=instance)

@receiver(post_save, sender=Word)
def create_user_word(sender, instance, created, **kwargs):
    if created:
        UserWords.objects.create(user=instance.owner, word=instance, category=instance.category)

@receiver(post_save, sender=Question)
def create_user_question(sender, instance, created, **kwargs):
    if created:
        UserQuestions.objects.create(user=instance.owner, question=instance)
        