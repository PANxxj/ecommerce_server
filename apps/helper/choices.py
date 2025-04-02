from . import keys
from django.utils.translation import gettext_lazy as _
from django.db import models

class Gender(models.TextChoices):
    MALE = keys.MALE, _(keys.MALE)
    FEMALE = keys.FEMALE, _(keys.FEMALE)
    OTHER = keys.OTHER, _(keys.OTHER)
    
class UserType(models.TextChoices):
    VENDER = keys.VENDER, _(keys.VENDER)
    CUSTOMER = keys.CUSTOMER, _(keys.CUSTOMER)
    

class OrderStatus(models.TextChoices):
    PENDING = keys.PENDING,_(keys.PENDING)
    PROCESSING = keys.PROCESSING,_(keys.PROCESSING)
    SHIPPED = keys.SHIPPED,_(keys.SHIPPED)
    DELIVERED = keys.DELIVERED,_(keys.DELIVERED)
    CANCELED = keys.CANCELED,_(keys.CANCELED)
    
    
class PaymentStatus(models.TextChoices):
    PAID = keys.PAID,_(keys.PAID)
    PENDING = keys.PENDING,_(keys.PENDING)
    FAILED = keys.FAILED,_(keys.FAILED)
    
