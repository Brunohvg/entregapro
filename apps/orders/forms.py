from .models import Order
from apps.customers.models import Customer
from django.forms import ModelForm

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["full_name","nickname", 'document', 'email']
