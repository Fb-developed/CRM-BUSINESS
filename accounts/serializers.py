from rest_framework import serializers
from .models import CustomUser, EmailConfirmation, UserProfile
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.conf import settings
import random

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.is_active = False
        user.is_confirmed = False
        user.save()

        code = EmailConfirmation.create_hashed_code(user, code_type='register')
        self.send_code_to_email(user.email, code)
        return user

    def send_code_to_email(self, email, code):
        send_mail(
            subject="Код подтверждения",
            message=f"Ваш код: {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )


class ConfirmCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        code = data['code']
        confirmations = EmailConfirmation.objects.filter(code_type='register')

        for confirmation in confirmations:
            if confirmation.check_code(code):
                if confirmation.is_expired():
                    confirmation.delete()
                    raise serializers.ValidationError("Срок действия кода истёк.")
                data['user'] = confirmation.user
                data['confirmation'] = confirmation
                return data

        raise serializers.ValidationError("Неверный код.")

    def save(self):
        user = self.validated_data['user']
        confirmation = self.validated_data['confirmation']
        user.is_active = True
        user.is_confirmed = True
        user.save()
        confirmation.delete()


        

class ResendConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")
        if user.is_confirmed:
            raise serializers.ValidationError("Email уже подтверждён.")
        self.user = user
        return value

    def save(self):
        EmailConfirmation.objects.filter(user=self.user, code_type='register').delete()
        code = EmailConfirmation.create_hashed_code(self.user, code_type='register')
        send_mail(
        subject="Повторный код подтверждения",
        message=f"Ваш код: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[self.user.email],
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
        if not user.is_active:
            raise serializers.ValidationError('Аккаунт неактивен.')
        
        data['user'] = user
        return data

    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def save(self):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        EmailConfirmation.objects.filter(user=user, code_type='reset').delete()
        code = EmailConfirmation.create_hashed_code(user, code_type='reset')
        send_mail(
            subject="Код для сброса пароля",
            message=f"Ваш код: {code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
    )



class PasswordResetConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают."})

        # Поиск подтверждения по коду
        confirmations = EmailConfirmation.objects.filter(code_type='reset')
        for confirmation in confirmations:
            if confirmation.check_code(data['code']):
                if confirmation.is_expired():
                    confirmation.delete()
                    raise serializers.ValidationError({"code": "Срок действия кода истёк."})
                data['user'] = confirmation.user
                data['confirmation'] = confirmation
                return data

        raise serializers.ValidationError({"code": "Неверный код."})

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()
        self.validated_data['confirmation'].delete()





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
        fields = ['firstname', 'lastname', 'image', 'gender', 'phone_number']