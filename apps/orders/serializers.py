from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from apps.products.serializers import ProductSerializer


class CartItemSerializers(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    