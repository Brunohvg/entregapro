# your_project/core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order # Assumindo que Order está na app 'orders'
from django.views import View
from apps.customers.models import Customer
from apps.customers.forms import CustomerForm
from django.utils.decorators import method_decorator
from apps.orders.forms import OrderForm
from apps.customers.forms import CustomerForm, AddressForm

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




@method_decorator(login_required, name='dispatch')
class OrderCreated(View):
    def get(self, request):
        context = {
            "form": OrderForm(),
            "form_customer": CustomerForm(),
            "form_address": AddressForm(),
        }
        return render(request, 'orders/order_created.html', context)

    def post(self, request):
        document = request.POST.get('document')
        customer = Customer.objects.filter(document=document).first()

        form = OrderForm(request.POST)
        form_address = AddressForm(request.POST)

        if customer:
            # Cliente já existe
            if form.is_valid() and form_address.is_valid():
                address = form_address.save(commit=False)
                address.customer = customer
                address.save()

                order = form.save(commit=False)
                order.customer = customer
                order.save()

                return redirect('orders:order_list')

        else:
            # Novo cliente
            form_customer = CustomerForm(request.POST)
            if form.is_valid() and form_customer.is_valid() and form_address.is_valid():
                customer = form_customer.save()

                address = form_address.save(commit=False)
                address.customer = customer
                address.save()

                order = form.save(commit=False)
                order.customer = customer
                order.save()

                return redirect('orders:order_list')
        # Em caso de erro
        context = {
            "form": form,
            "form_customer": form_customer if not customer else CustomerForm(),
            "form_address": form_address,
        }
        return render(request, 'orders/order_created.html', context)
