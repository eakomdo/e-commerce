from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CUSTOMER = 'customer', 'Customer'
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(max_length=20)
    profile_picture = models.ImageField(upload_to='Me/profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default='CUSTOMER')
    is_verified = models.BooleanField(default=False)
    is_activen = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FILED = 'email'
    REQUIRED_FIELDS = ['firstname', 'last_name']
    
    def __str__(self):
        return self.email
    
    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def is_admin(self):
        return self.Role == self.Role.ADMI