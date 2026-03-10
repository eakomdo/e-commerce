from django.db import models
from autoslug import AutoSlugField


#Categories Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', always_update=False, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_plural_name = 'Categories'
        
        def __str__(self):
            return self.tile
        