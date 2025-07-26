# ARQUIVO: apps/orders/templatetags/order_helpers.py
# OBJETIVO: Definir filtros personalizados para usar nos templates do app de pedidos.

from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplica o valor (value) pelo argumento (arg)."""
    try:
        # Tenta converter para float para garantir que a multiplicação funcione
        return float(value) * float(arg)
    except (ValueError, TypeError):
        # Retorna uma string vazia se a conversão falhar
        return ''

@register.filter(name='status_to_badge')
def status_to_badge(status_key):
    """Converte a chave do status do pedido em uma classe de badge Bootstrap."""
    status_map = {
        'PENDING': 'bg-info text-dark',        # Pedido pendente → azul claro
        'PAID': 'bg-success',                  # Pago → verde
        'REFUSED': 'bg-danger',                # Recusado → vermelho
        'PICKED_UP': 'bg-primary',             # Retirado → azul escuro
        'ON_THE_WAY': 'bg-warning text-dark',  # A caminho → amarelo
        'DELIVERED': 'bg-success',             # Entregue → verde
        'FAILED': 'bg-danger',                 # Falhou → vermelho
        'CANCELLED': 'bg-secondary',           # Cancelado → cinza
    }
    return status_map.get(status_key, 'bg-light text-dark')  # Default → fundo claro


