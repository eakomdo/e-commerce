import django_filters
from .models import Product, Category


class ProductFilter(django_filters.filterset):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    Category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    is_available = django_filters.BooleanFilter(field_name='is_available')
    search = django_filters.CharFilter(method='filter_search', label='Search')
    has_discount = django_filters.BooleanFilter(method='filter_has_discount', label='Has discount')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock', label='in stock')
    
    class Meta:
    model = Product
    fields = [
        'category',
        'is_available',
        'min_price',
        'max_price',
        'search',
        'has_discount',
        'in_stock',
    ]
    
    
    def filter_search(self, queryset, name, value):
        from django.db.models import Q
        
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
    
    def filter_has_discount(self, queryset, name, value):
        if value:
            return queryset.filter(discount_price__isnull=False)
        return queryset.filter(discount_price__isnull=True)
    
    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)