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
        
class SimpleCatrgotySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        
class ProductSerialiser(serializers.ModelSerializer):
    category = SimpleCatrgotySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all() , source='category', write_only=True)
    image = ProductImageSerializer(many=True, write_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.FloatField(read_only=True)
    
      class Meta:
        model = Product
        fields = [
            'id',
            'category',      
            'category_id',     
            'name',
            'slug',
            'description',
            'price',
            'discount_price',
            'effective_price',  
            'discount_percentage',  
            'stock',
            'is_in_stock',      
            'image',
            'images',           
            'is_available',
            'created_at',
        ]
        
        
        def validate_price(self, value):
            if 
    
    