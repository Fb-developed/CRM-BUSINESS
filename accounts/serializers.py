from rest_framework import serializers
from .models import CustomUser, EmailConfirmation, UserProfile
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True},}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        confirmation = EmailConfirmation.objects.create(user=user)
        self.send_confirmation_email(user.email, confirmation.token)
        return user

    def send_confirmation_email(self, email, token):
        confirm_link = f"http://127.0.0.1:8000/auth/confirm-email/{token}"
        send_mail(
            subject="Подтвердите ваш email",
            message=f"Перейдите по ссылке для подтверждения: {confirm_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Неверное имя пользователя или пароль.')
        if not user.is_confirmed:
            raise serializers.ValidationError('Email не подтвержден.')
        
        data['user'] = user
        return data

    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        EmailConfirmation.objects.filter(user=user).delete()
        
        token = EmailConfirmation.objects.create(user=user)
        reset_link = f"http://127.0.0.1:8000/auth/reset-password-confirm/{token.token}/"
        send_mail(
            subject="Сброс пароля",
            message=f"Перейдите по ссылке для сброса пароля: {reset_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают."})
        return data

    def save(self):
        token = self.validated_data['token']
        password = self.validated_data['password']
        
        try:
            token_obj = EmailConfirmation.objects.get(token=token)
        except EmailConfirmation.DoesNotExist:
            raise serializers.ValidationError({"token": "Неверный токен."})
        
        if token_obj.is_expired():
            token_obj.delete()
            raise serializers.ValidationError({"token": "Срок действия токена истек."})
        
        user = token_obj.user
        user.set_password(password)
        user.save()
        token_obj.delete()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only = True)
    new_password_confirm = serializers.CharField(write_only = True)

    def validate_old_password(self, data):
        user = self.context['request'].user
        if not user.check_password(data):
            raise serializers.ValidationError("Неверный текущий пароль")
        return data
    
    def save(self, **kwargs):
        new_password = self.validated_data['new_password']
        new_password_confirm = self.validated_data['new_password_confirm']

        if new_password != new_password_confirm:
            raise serializers.ValidationError({"new_password_confirm": "Пароли не совпадают."})

        user = self.context['request'].user
        user.set_password(new_password)
        user.save()
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'image', 'gender', 'phone_number', 'bio']