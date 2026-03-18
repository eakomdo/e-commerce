from django.db import models
from apps.users.models import User
from apps.products.models import Product


# cart model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

    @property
    def total_item(self):
        return self.aggregate.items.all(total=models.Sum("quantity")["total"] or 0)

    @property
    def total_price(self):
        total = Sum(
            item.product.effective_price * item.quantity for item in self.items.all()
        )
        return round(total, 2)
    
#Cart Item model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    class Meta:
        unique_together = ['cart', 'product']
        
    @property
    def subtotal(self):
        return round(self.product.effective_price * self.quantity, 2)
    
#Order model
class Order(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
        
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
        status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
        total_amount = models.DecimalField(max_digits=10, decimal_places=2)
        shipping_address = models.CharField()
        shipping_country = models.CharField(max_length=20)
        shipping_city = models.CharField(max_length=20)
        notes = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return f'Order of #{self.id} by {self.user.email}'
        
        class Meta:
            ordering = ['-created_at']
            
        @property
        def is_cancellable(self):
            return self.status == Status.PENDING
    
#order item model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    Product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='order_item')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in order #{self.order.id}'