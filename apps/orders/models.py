from django.db import models
from apps.customers.models import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, default='pending')
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Verifica se é uma criação (não edição)


        super().save(*args, **kwargs)  # Salva o pedido primeiro

        # Se for novo pedido, atualiza o total gasto do cliente
        if is_new:
            self.customer.spent_total += self.total_amount
            self.customer.save()
            
    def delete(self, *args, **kwargs):
        # Subtrai o valor do pedido do total gasto do cliente
        self.customer.spent_total -= self.total_amount
        self.customer.save()

        print(f"Pedido {self.order_number} será deletado")
        super().delete(*args, **kwargs)



    def __str__(self):
        return f"Order #{self.order_number} - {self.customer.full_name}"
