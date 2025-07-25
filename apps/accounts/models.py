from django.db import models
sum

# Create your models here.
class UserType(models.TextChoices):
    MANAGER = 'MANAGER', 'Supervisor'
    CUSTOMER = 'CUSTOMER', 'Cliente'
    DELIVERY_PERSON = 'DELIVERY_PERSON', 'Motoboy'

