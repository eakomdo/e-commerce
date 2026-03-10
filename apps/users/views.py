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
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        # is_valid() runs all our validation checks
        # raise_exception=True automatically returns 400 if invalid
        if serializer.is_valid(raise_exception=True):

            # Save the user — this calls our create() method in the serializer
            user = serializer.save()

            # Generate email verification token
            token = default_token_generator.make_token(user)

            # Encode user id so we can safely put it in a URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build verification link
            # Frontend will hit this link when user clicks verify
            verification_link = f"http://localhost:8000/api/users/verify-email/?uid={uid}&token={token}"

            # TODO: send this link via email (we'll do this in notifications app)
            # For now just return it in the response so we can test
            print(f"Verification link: {verification_link}")

            return Response({
                'message': 'Registration successful. Please verify your email.',
                'verification_link': verification_link  # remove this in production
            }, status=status.HTTP_201_CREATED)
        
        
#verify email endpoint
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        
        if not uid or not token:
            return Response({'message': 'Missing uid or token'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            #find user
            user = User.objects.get(pk=user_id)
            
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({'message': 'Invalid link or url has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_verified = True
        user.save()
        
        return Response({'message': 'Email has been verified successfully'}, status=status.HTTP_200_OK)
    

#login endpoint
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data('user')
            tokens = get_token_for_user(user)
            
            return Response({'message': 'Login successful', 'tokens': tokens, 'User': UserSerializer(user).data}, status=status.HTTP_200_OK)
        

#user profile endpoint/ uapdating 
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #updating profile
    def put(self, requst):
        serializer = UserSerializer(
            request.user,
            data=self.request.data,
            partial = True
        )
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response({'message': 'Profile updated successfully', 'User': serializer.data}, status=status.HTTP_200_OK)


#password request link endpoint
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        serializer = PasswordResetRequestSerialiazer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data('user')
            user = User.objects.get(email=email)
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            #reset link
            reset_link = f"http://localhost:8000/api/users/password-reset-confirm/?uid={uid}&token{token}"
            
            return Response({'message': 'Password reset link has been sent to your mail'}, status=status.HTTP_200_OK)
    

#password reset confirm endpoint
class PasswordConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirm(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            uid = request.query_params.get(user)
            token = request.query_params.get(token)
            
            try:
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)
                
            except(User.DoesNotExist, ValueError):
                return Response({'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
            
            #check if token is valid
            if not default_token_generator.check_token(user, token):
                return Response({'message': 'Invalid link or token has expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.get_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'message': 'Password Reset Successfully'}, status=status.HTTP_200_OK)