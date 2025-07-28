# your_project/core/views.py
from ast import Or
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.orders.forms import OrderForm
from apps.orders.models import Order

from apps.customers.forms import CustomerForm, AddressForm
from apps.orders.utils.orders import (get_customer_by_document, handle_existing_customer, handle_new_customer,)

from .models import Order, Customer

from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        orders = super().get_queryset().order_by('customer')
        search = self.request.GET.get('search')
        if search:
            orders = orders.filter(order_number__icontains=search)
        return orders

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
        customer = get_customer_by_document(document)

        form = OrderForm(request.POST)
        form_address = AddressForm(request.POST)
        form_customer = CustomerForm(request.POST)

        if customer:
            success = handle_existing_customer(customer, form, form_address)
        else:
            success = handle_new_customer(form_customer, form_address, form)

        if success:
            return redirect('orders:order_list')

        context = {
            "form": form,
            "form_customer": form_customer if not customer else CustomerForm(),
            "form_address": form_address,
        }
        return render(request, 'orders/order_created.html', context)


# your_project/orders/views.py


class OrderDetailView(DetailView):
    """
    View para exibir os detalhes de um único pedido.
    Utiliza DetailView do Django para buscar um objeto Order
    e passá-lo para o template.
    """
    model = Order
    template_name = 'orders/order_detail.html' # O template principal para esta view
    context_object_name = 'order' # O nome da variável de contexto que será usada no template

    def get_context_data(self, **kwargs):
        """
        Adiciona dados adicionais ao contexto do template.
        Neste caso, tentamos obter o endereço principal do cliente do pedido.
        """
        context = super().get_context_data(**kwargs)
        order = self.get_object() # Obtém o objeto Order atual
        
        # Tenta obter o endereço principal do cliente associado ao pedido
        # Se o cliente tiver múltiplos endereços, você pode ajustar a lógica aqui
        # para selecionar o endereço relevante para o pedido (se houver um link direto)
        # ou apenas listar todos os endereços do cliente.
        # Para este exemplo, vamos tentar pegar o endereço marcado como primário.
        try:
            context['primary_address'] = order.customer.addresses.filter(is_primary=True).first()
        except Customer.addresses.RelatedObjectDoesNotExist:
            context['primary_address'] = None
        
        return context



from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Order

def gerar_etiqueta_pdf(request, pk):
    order = Order.objects.get(pk=pk)
    address = order.customer.addresses.first()  # acessa o primeiro endereço do cliente

    html_string = render_to_string("orders/includes/order_label.html", {
        "order": order,
        "primary_address": address
    })

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    return HttpResponse(pdf, content_type="application/pdf")
