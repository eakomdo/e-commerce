from django.db import models
from apps.users.models import User

#cart model
class Cart(models.Model):
    user = models.ForeignKey(User)