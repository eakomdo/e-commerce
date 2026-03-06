from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


# user registration
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        field = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        ]


def validate(self, attrs):
    if attrs["password"] != attrs["confirm_password"]:
        raise serializers.ValidationError("Passwords do no match")
    return attrs


def create(self, validated_data):
    validated_data.pop("confirm_password")
    user = User.objects.create_user(**validated_data)
    return user


# login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        self.password = attrs.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid Email or Password")

        if not user.is_verified:
            raise serializers.ValidationError("Please verify your email first")

        if not user.is_active:
            raise serializers.ValidationError("Your account is disabled")

        attrs["user"] = user

        return attrs
    
    #user serializer
    class UserSerialiazer(serializers.ModelSerializer):
        full_name = serializers.CharField(read_only=True)
        
        class Meta:
            model = User
            fields = ['id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'profile_picture',
            'role',
            'is_verified',
            'created_at',]
            
            read_only_fields = ['id', 'email', 'role', 'is_verified', 'created_at']

#password reset request serializer
class PasswordResetRequestSerialiazer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email not found')
        return value
    
#password reset  confirm
class PasswordResetConfirm(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
         if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
         return attrs   