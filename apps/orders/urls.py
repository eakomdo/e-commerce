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

url_patterns =[
        # GET → get current cart
    path('cart/', CartView.as_view(), name='cart'),
]