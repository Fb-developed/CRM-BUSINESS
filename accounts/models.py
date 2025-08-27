from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_confirmed = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



class EmailConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, related_name='confirmation', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = self.created_at + timedelta(hours=24)
        return timezone.now() > expiration_time


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('W', 'Женский'),
    ]
    user = models.OneToOneField(CustomUser,  related_name='user_profile', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserProfile'