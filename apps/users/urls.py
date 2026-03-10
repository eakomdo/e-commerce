from django.urls import path
from .views import (
    RegistrationView,
    VerifyEmailView,
    LoginView,
    UserProfileView,
    PasswordResetRequestView,
    PasswordConfirmView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordConfirmView.as_view(), name='password-reset-confirm')
]
