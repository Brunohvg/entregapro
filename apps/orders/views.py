# your_project/core/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order # Assumindo que Order está na app 'orders'
from apps.customers.models import Customer # Assumindo que Customer está na app 'customers'
from django.views import View


class OrderList(View):
    def get(self, request):
        orders = Order.objects.all().select_related('customer') # 'select_related' para otimizar o acesso ao customer
        search = request.GET.get('search')
        if search:
            orders = orders.filter(order_number__icontains=search)
        context = {
            'orders': orders
        }
        return render(request, 'orders/order_list.html', context)

    

