from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    CheckoutView,
    OrderListView,
    OrderDetailView,
    CancelOrderView
)

app_name ='orders'
