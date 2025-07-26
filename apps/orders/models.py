# your_project/orders/models.py (assumindo que você tenha uma app 'orders' ou similar)

from django.db import models
from apps.customers.models import Customer
from django.db.models import Sum
from django.utils import timezone

class DeliveryStatus(models.TextChoices):
    PENDING = "PENDING", "Aguardando coleta"
    PICKED_UP = "PICKED_UP", "Coletado pelo motoboy"
    ON_THE_WAY = "ON_THE_WAY", "Em rota de entrega"
    DELIVERED = "DELIVERED", "Entregue ao destinatário"
    FAILED = "FAILED", "Entrega não realizada"
    RETURNED = "RETURNED", "Pedido devolvido ao remetente"
    CANCELLED = "CANCELLED", "Entrega cancelada"


class PaymentStatus(models.TextChoices):

    PENDING = "PENDING", "Aguardando pagamento"
    PAID = "PAID", "Pagamento aprovado"
    REFUSED = "REFUSED", "Pagamento recusado"



class Order(models.Model):  # TABELA PEDIDO
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Nº Pedido')
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name='Status Pagamento'
    )
    delivery_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
        verbose_name='Status Entrega' # Adicionado verbose_name aqui
    )
    total_amount = models.FloatField(verbose_name='Valor Total') # Adicionado verbose_name
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado Em') # Adicionado verbose_name
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado Em') # Adicionado verbose_name

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at'] # Ordenar por data de criação decrescente

    def __str__(self):
        return f"Pedido #{self.order_number} - {self.customer.full_name}"
    
    def total_orders_month(year=None, month=None):
        """
        Retorna a soma do total_amount dos pedidos no mês e ano informados.
        Se não informar, usa o mês e ano atuais.
        
        :param year: Ano (int), ex: 2025
        :param month: Mês (int), ex: 7
        :return: Float com soma dos pedidos
        """
        now = timezone.now()
        year = year or now.year
        month = month or now.month

        return Order.objects.filter(
            created_at__year=year,
            created_at__month=month
        ).aggregate(total=Sum("total_amount"))["total"] or 0