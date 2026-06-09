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
    #get current cart
    path('cart/', CartView.as_view(), name='cart'),
    
    #add item to cart
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    
    #update and delete cart
    path('cart/items/<int:item_id>/', UpdateCartItemView.as_view(), name='update-cart'),
    
    #checkout order - covert cart to order
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    #view/get order 
    path('', OrderListView.as_view(), name='')
    
    #get a specific order 
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail')
    
    #cancel order
    path('<int:order_id>/cancel/', CancelOrderView.as_view(), name='cancel-order')
    
]