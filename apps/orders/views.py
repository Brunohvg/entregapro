# your_project/core/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order # Assumindo que Order está na app 'orders'
from apps.customers.models import Customer # Assumindo que Customer está na app 'customers'


@login_required
def order_list(request):
    """
    View para listar todos os pedidos.
    """
    orders = Order.objects.all().select_related('customer') # 'select_related' para otimizar o acesso ao customer
    context = {
        'orders': orders
    }
    return render(request, 'orders/order_list.html', context)
