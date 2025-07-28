from .models import Order
from apps.customers.models import Customer
from django.forms import ModelForm

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'payment_status', 'delivery_status', 'total_amount', 'observations']
