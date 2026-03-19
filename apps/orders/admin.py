from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_amount', 'created_at']
    list_filters = ['status']
    search_fields = ['user__email']
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    