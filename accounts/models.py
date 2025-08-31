from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password
import random

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_confirmed = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



class EmailConfirmation(models.Model):
    CODE_TYPE_CHOICES = [
        ('register', 'Регистрация'),
        ('reset', 'Сброс пароля'),
    ]
    user = models.ForeignKey(CustomUser, related_name='confirmation', on_delete=models.CASCADE)
    code = models.CharField(max_length=128)
    code_type = models.CharField(max_length=10, choices=CODE_TYPE_CHOICES, default='register')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    @staticmethod
    def generate_raw_code():
        return f"{random.randint(100000, 999999)}"

    @classmethod
    def create_hashed_code(cls, user, code_type='register'):
        raw_code = cls.generate_raw_code()
        hashed_code = make_password(raw_code)
        cls.objects.create(user=user, code=hashed_code, code_type=code_type)
        return raw_code  # возвращаем для отправки по email
    
    def check_code(self, raw_code):
        return check_password(raw_code, self.code)
    
    @classmethod
    def verify_code(cls, user, raw_code, code_type='register'):
        confirmations = cls.objects.filter(user=user, code_type=code_type)
        for confirmation in confirmations:
            if confirmation.check_code(raw_code):
                if confirmation.is_expired():
                    confirmation.delete()
                    return None
                return confirmation
        return None

            
    @classmethod
    def delete_expired(cls):
        cls.objects.filter(created_at__lt=timezone.now() - timedelta(minutes=5)).delete()



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
    phone_number = models.CharField(max_length=255, blank=True, validators=[RegexValidator(r'^\+?\d{9,15}$', 'Введите корректный номер телефона')])
    age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserProfile'