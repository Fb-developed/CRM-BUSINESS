from django.shortcuts import render
from rest_framework import generics, permissions
from .models import CustomUser, UserProfile
from rest_framework.response import Response
from .models import CustomUser, EmailConfirmation
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, ChangePasswordSerializer, UserProfileSerializer
from rest_framework import status       
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class ConfirmEmailView(APIView):
    def get(self, request, token):
        try:
            confirm = EmailConfirmation.objects.get(token = token)
            user = confirm.user
            user.is_confirmed = True
            user.is_active =True
            user.save()
            confirm.delete()
            return Response({'message':'Email confirmed.'}, status=status.HTTP_200_OK)
        except EmailConfirmation.DoesNotExist:
            return Response({'errors':'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer( data = request.data )

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
            }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Ссылка для сброса пароля отправлена на почту.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        data = request.data.copy()
        data['token'] = token
        serializer = PasswordResetConfirmSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Пароль успешно изменён'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пароль успешно изменён."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    


