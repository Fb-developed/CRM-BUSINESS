from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid


class CustomUser(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    password = models.TextField()
    is_confirmed = models.BooleanField()

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class EmailConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, related_name='confirmation', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,  related_name='user_profile', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    image = models.BigIntegerField()
    gender = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField()
    created_at = models.DateField()

    class Meta:
        db_table = 'UserProfile'