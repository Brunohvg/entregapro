from django.db import models

class Customer(models.Model): # TABELA CLIENTE 
    full_name = models.CharField(max_length=255, verbose_name='Nome Completo')
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome ou Apelido')
    document = models.CharField(max_length=50, unique=True, verbose_name='Cpf ou Cnpj')
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='E-mail')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    spent_total = models.FloatField(default=0.0, blank=True, null=True, verbose_name='Total Gasto')

    def __str__(self):
        return self.full_name


class Address(models.Model): # TABELA ENDEREÇO
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255, verbose_name='Rua')
    number = models.CharField(max_length=20, verbose_name='Numero')
    complement = models.CharField(max_length=255, blank=True, null=True, verbose_name='Complemento')
    neighborhood = models.CharField(max_length=100, verbose_name='Bairro')
    city = models.CharField(max_length=100, verbose_name='Cidade')
    postal_code = models.CharField(max_length=20, verbose_name='Cep')
    reference = models.CharField(max_length=255, blank=True, null=True, verbose_name='Referencia')
    is_primary = models.BooleanField(default=False, verbose_name='Endereço principal')


    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}"
