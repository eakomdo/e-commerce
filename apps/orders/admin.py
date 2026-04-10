from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filters = ['status']
    search_fields = ['user__email']
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'created_at']
    

admin.site.register(CartItem)
admin.site.register(OrderItem