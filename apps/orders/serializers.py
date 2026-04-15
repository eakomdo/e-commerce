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
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializers(many=True, read_only=True)
    
    total_item = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'total_items',
            'total_price',
            'created_at',
            'updated_at'
        ]
        
        read_only_fields = ['id', 'created_at', 'updated_at']
        
#add to cart serializer
class AddToCartSerializer(serializers.Serializer):
    
    #we get the item by id and ceck if it is available or in stock before updating cart
    def validate_product_id(self, value):
        
        from apps.products.models import Product
        
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product cannot be found')
        
        
        if not product.is_available:
            raise serializers.ValidationError('Product is not available')
        
        if not product.is_in_stock:
            raise serializers.ValidationError('Produt is not in stock')
        return value
     
     
    #check the requested quantity does not exceed what's in stock   
    def validate(self, attrs):
        
        from apps.products.models import Product
        
        product = Product.objects.get(id=attrs['product_id'])
        
        if attrs['quantity'] > product.stock:
            raise serializers.ValidationError({f'Only {product.stock} items available in stock'})
        return attrs 
        

#order item serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta: 
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'price',
            'subtotal'
        ]
        
        read_only_fields = ['id', 'price']
        

#order serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    is_cancellable = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'status_display',
            'items',
            'total_amount',
            'shipping_address',
            'shipping_country',
            'shipping_city',
            'notes',
            'is_cancellable',
            'created-at',
            'upadated_at'
        ]
        
        read_only_fields = [
            'id',
            'status',
            'total_amount',
            'created_at',
            'updated_at'
        ]

#checkout serializer
class CheckoutSerializer(serializers.ModelSerializer):
    shipping_country = serializers.CharField(max_length=100)
    shipping_city = serializers.CharField(max_length=100)
    shipping_address = serializers.charfield(max_lenght=100)
    
    def validate(self, attrs):