# apps/couriers/models.py
from django.db import models

class Courier(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome do motoboy')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')

    def __str__(self):
        return self.name or "Entregador sem nome"
