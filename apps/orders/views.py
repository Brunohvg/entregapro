# Standard Library


# Django Core
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy

# Third-Party
from weasyprint import HTML

# Local Apps
from apps.orders.forms import OrderForm
from apps.orders.models import Order
from apps.orders.utils.orders import handle_existing_customer, handle_new_customer
from apps.customers.forms import CustomerForm, AddressForm
from apps.customers.utils.customers import get_customer_by_document
from apps.customers.models import Customer
from apps.orders.utils.generate_pdf import generate_pdf



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

@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    """
    View para exibir os detalhes de um único pedido.
    """
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        """
        Otimiza as queries para carregar customer e seus endereços de uma vez.
        """
        return Order.objects.select_related('customer').prefetch_related('customer__addresses')

    def get_context_data(self, **kwargs):
        """
        Adiciona o endereço principal do cliente ao contexto.
        """
        context = super().get_context_data(**kwargs)
        order = self.object  # já está disponível no DetailView
        customer = getattr(order, 'customer', None)

        if customer:
            context['primary_address'] = customer.addresses.filter(is_primary=True).first()
        else:
            context['primary_address'] = None

        return context

@method_decorator(login_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    context_object_name = 'order'
    template_name = 'orders/order_created.html'  # ou outro template

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Pedido atualizado com sucesso!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    


def generate_label_pdf(request, pk):
    return generate_pdf(request, pk)
