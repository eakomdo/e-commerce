from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


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

