from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    ProductImageUploadView
)

app_name = 'products'

urlpatterns = [
   
    #list all categories, create a category (admin only)
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),

    #get single category by slug, update category (admin only), delete category (admin only)
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    #list all products (supports filtering)
    #create a product (admin only)
    path('', ProductListCreateView.as_view(), name='product-list'),

    #get single product by slug
    #update product (admin only)
    #delete product (admin only)
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),

    #upload images for a product (admin only)
    path('<slug:slug>/images/', ProductImageUploadView.as_view(), name='product-images'),
]