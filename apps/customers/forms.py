from django import forms
from django.forms import ModelForm
from apps.customers.models import Customer, Address

from django.core.exceptions import ValidationError
from django.utils.text import slugify

def input_widget(placeholder):
    return forms.TextInput(attrs={'class': 'form-control', 'placeholder': placeholder})

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'nickname', 'phone', 'email', 'document']
        labels = {
            'full_name': 'Nome Completo',
            'nickname': 'Nome ou Apelido',
            'phone': 'Celular',
            'email': 'E-mail',
            'document': 'CPF ou CNPJ',
        }
        widgets = {
            'full_name': input_widget('Nome completo'),
            'nickname': input_widget('Apelido'),
            'phone': input_widget('(99) 99999-9999'),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'cliente@email.com'}),
            'document': input_widget('000.000.000-00'),
        }




class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'complement', 'neighborhood', 'city', 'postal_code', 'reference']

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # Normaliza os campos removendo espaços extras e colocando em minúsculas
        def normalize(value):
            return slugify(value or '').replace('-', ' ').strip()

        street = normalize(cleaned_data.get('street'))
        number = normalize(cleaned_data.get('number'))
        complement = normalize(cleaned_data.get('complement'))
        neighborhood = normalize(cleaned_data.get('neighborhood'))
        city = normalize(cleaned_data.get('city'))
        postal_code = normalize(cleaned_data.get('postal_code'))

        if self.customer:
            existing = Address.objects.filter(customer=self.customer)
            for addr in existing:
                if (
                    normalize(addr.street) == street and
                    normalize(addr.number) == number and
                    normalize(addr.complement) == complement and
                    normalize(addr.neighborhood) == neighborhood and
                    normalize(addr.city) == city and
                    normalize(addr.postal_code) == postal_code
                ):
                    raise ValidationError("Este endereço já foi cadastrado para este cliente.")

        return cleaned_data
