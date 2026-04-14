from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from apps.products.serializers import ProductSerializer


class CartItemSerializers(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    
    product_id = serializerS.PrimaryKeyRelatedField(
        source='product',
        read_only=True
    )
    
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta: 
        model = CartItem
        fields = [
            'id',
            'product',
            'product_id',
            'quantity',
            'subtotal',
            'added_at'
        ]
        read_only_fields = ['id', 'added_at']
        
        