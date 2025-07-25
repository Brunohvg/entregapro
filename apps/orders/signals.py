from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Order
from apps.customers.models import Customer
from django.db.models import Sum

# Guarda o status anterior do pedido antes de salvar
@receiver(pre_save, sender=Order)
def salvar_status_antigo(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_payment_status = Order.objects.get(pk=instance.pk).payment_status
        except Order.DoesNotExist:
            instance._old_payment_status = None
    else:
        instance._old_payment_status = None


def atualizar_total_gasto_cliente(cliente):
    total = Order.objects.filter(customer=cliente, payment_status="PAID").aggregate(
        total=Sum("total_amount")
    )["total"] or 0.0
    cliente.spent_total = total
    cliente.save()


@receiver(post_save, sender=Order)
def atualizar_total_gasto_on_save(sender, instance, **kwargs):
    old = getattr(instance, "_old_payment_status", None)
    if instance.payment_status != old:
        atualizar_total_gasto_cliente(instance.customer)


@receiver(post_delete, sender=Order)
def atualizar_total_gasto_on_delete(sender, instance, **kwargs):
    atualizar_total_gasto_cliente(instance.customer)
