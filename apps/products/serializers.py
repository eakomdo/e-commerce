from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Category,
    Product,
    ProductImage
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'caption']
        
    