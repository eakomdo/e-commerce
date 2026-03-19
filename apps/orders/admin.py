from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


@admin.register(Order)
class OrderAdmin(models.ModelAdmin)