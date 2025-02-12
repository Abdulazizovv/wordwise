from .models import BotUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
import logging


# Create a User instance when a BotUser instance is created
@receiver(post_save, sender=BotUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        if instance.phone_number and instance.first_name:
            if not User.objects.filter(phone_number=instance.phone_number).exists():
                User.objects.create(phone_number=instance.phone_number, first_name=instance.first_name)
                logging.info(f'User created with phone number {instance.phone_number}')
            else:
                logging.info(f'User with phone number {instance.phone_number} already exists')
        else:
            logging.error('User not created, missing phone number or first name')
    else:
        logging.info('BotUser updated, no action taken')