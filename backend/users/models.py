from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from botapp.models import BotUser


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        if not first_name:
            raise ValueError('The First Name must be set')

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, password=None, **extra_fields):
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    phone_number = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = None
    # email = models.EmailField(unique=True, null=True, blank=True)
    tg_account = models.OneToOneField(BotUser, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.first_name