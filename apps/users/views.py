from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
    PasswordResetConfirm,
    PasswordResetRequestSerialiazer,
)

#generating jwt token
def generate_jwt_token(User):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
    
#registrstion endpoint
def post (self, request):
    