from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from .serializers import CartItemSerializers, CartSerializer, AddToCartSerializer, OrderItemSerializer, OrderSerializer,CheckoutSerializer
from apps.products.models import models


#returns the current user's cart
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(request=request.user)
        
        serialzer = CartSerializer(cart, context={'request' : request})
        return Response(serialzer.data, status=status.HTTP_200_OK)
    
#add to cart 
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = AddToCartSerializer(data=request.data)