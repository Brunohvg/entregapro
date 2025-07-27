# ARQUIVO: apps/orders/templatetags/order_helpers.py

from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplica o valor (value) pelo argumento (arg)."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter(name='status_to_badge')
def status_to_badge(status_key):
    """Converte a chave do status do pedido em uma classe de badge Bootstrap."""
    status_map = {
        'PENDING': 'rounded-pill bg-warning-subtle text-warning border-warning border',
        'PAID': 'rounded-pill bg-success-subtle text-success border-success border',
        'REFUSED': 'rounded-pill bg-danger-subtle text-danger border-danger border',
        'PICKED_UP': 'rounded-pill bg-indigo-subtle text-indigo border-indigo border',
        'ON_THE_WAY': 'rounded-pill bg-info-subtle text-info border-info border',  # MUDANÇA: Azul claro
        'DELIVERED': 'rounded-pill bg-success-subtle text-success border-success border',
        'FAILED': 'rounded-pill bg-danger-subtle text-danger border-danger border',
        'CANCELLED': 'rounded-pill bg-secondary-subtle text-secondary border-secondary border', # MUDANÇA: Cinza suave
        'RETURNED': 'rounded-pill bg-dark-subtle text-dark border-dark border', # EX: Novo status com cor escura
    }
    return status_map.get(status_key, 'rounded-pill bg-secondary-subtle text-secondary border-secondary border') # Retorna cinza suave por padrão