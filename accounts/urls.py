from django.urls import path
from .views import RegisterView, ConfirmCodeView, LoginView, LogoutView, PasswordResetConfirmView, PasswordResetRequestView, ChangePasswordView, UserProfileView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)



urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-code/', ConfirmCodeView.as_view(), name='confirm-code'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]