from django.db import models
from apps.users.models import User
from apps.orders.models import Order
import uuid

#helper function to help generte a unique paymend id for each transaction
def generate_reference():
    return f"PAY-{uuid.uuid4}"