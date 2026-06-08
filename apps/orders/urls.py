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

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/items/<int:item_id>/', UpdateCartItemView.as_view(), name='update-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    
]