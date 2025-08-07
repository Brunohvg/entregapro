from django.forms import ModelForm
from models import Courier

class CourierForm(ModelForm):
    class Meta:
        model = Courier
        fields = ['name', 'phone',  'is_active', 'document',]