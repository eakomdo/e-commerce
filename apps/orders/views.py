from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem,
from .serializers import (
    CartItemSerializers,
    CartSerializer,
    AddToCartSerializer,
    OrderItemSerializer,
    OrderSerializer,
    CheckoutSerializer,
)
from apps.products.models import models


# returns the current user's cart
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(request=request.user)

        serialzer = CartSerializer(cart, context={"request": request})
        return Response(serialzer.data, status=status.HTTP_200_OK)


# add to cart
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AddToCartSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]

            # get the product
            product = Product.objects.get(id=product_id)

            # get or create cart for this user
            cart, _ = Cart.objects.get_or_create(user=request.user)

            # get existing cart item for this product
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product, 
                defaults={"quantity": quantity} #default is only applied when creating and ignored when item already exists 
            )
            
            #update item quantity if it already exist in cart
            if not item_created:
                cart_item.quantity +=quantity
                cart_item.save()
                
            #return updated cart
            serializer = CartItemSerializers(
                cart,
                context={'request': request}
            )
            
            return Response({
                'message': 'Item added to cart',
                'cart' : cart_serializer.data
            }, status=status.HTTP_201_CREATED)


#update and delete cart item
class UpdateCartItem(APIView):
permission_classes = [IsAuthenticated]

#search item
def get_object(self, item_id, user):
    return get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=user
    )
    
def put(self, request, item_id):
    cart_item = self.get_object(item_id, request.user)
    quantity = request.data.get('quantity')
    
    #check if quantity is less than 1
    if not quantity or int(quantity) < 1:
        return Response({
            'error': 'Quantity must be at least 1',
        }, status=status.HTTP_400_BAD_REQUEST)
        
    
    #check is item is available in stock
    if int(quantity) > cart_item.product.stock:
        return Response({
            'error': f'only {cart_item.product.stock} available'
        }status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = int(quantity)
        cart_item.save()
        
        cart_serializer = CartSerializer(
            cart_item.cart,
            context={'request': request}
        )
        
        return Response({
            'Cart updated!'
        }status=status.HTTP_200_OK)
        
        