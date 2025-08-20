from django.urls import path
from .views import RegisterView, ConfirmEmailView, LoginView, LogoutView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('confirm-email/<uuid:token>/', ConfirmEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]