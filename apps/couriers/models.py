from django.db import models


class Courier(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome do motoboy')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    document = models.CharField(max_length=20, blank=True, null=True, verbose_name='Documento')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return self.name or "Entregador sem nome"
