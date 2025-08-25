from django.urls import path
from .views import RegisterView, ConfirmEmailView, LoginView, LogoutView, PasswordResetConfirmView, PasswordResetRequestView, ChangePasswordView, UserProfileView
urlpatterns = [
    path('', RegisterView.as_view()),
    path('confirm-email/<uuid:token>/', ConfirmEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset-password/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password-confirm/<uuid:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),


]