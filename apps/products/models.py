from django.db import models
from autoslug import AutoSlugField


# Categories Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", always_update=False, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

        ordering = ["name"]


# products Model
class Product(models.Model):
    Category = models.ForeignKey(
        Category, on_delete=models.CASCADE, 
        related_name="products"
    )
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=False, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='Me/Images/product_images', blank=False, null=False)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

@property
def is_in_stock(self):
    return self.stock > 0

@property
def effective_price(self):
    return self.discount_price if self.discount_price else self.price


@property
def discount_percentage(self):
    if self.discount_price:
        discount = ((self.price - self.discount_price) / self.price) *100
        return round(discount, 2)
    return 0

#product image (multiples images per product)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='Me/Images/product_images')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    
    def __str__(self):
        return f'{self.product.name}- Image {self.order}'
    class Meta:
        ordering = ['order']