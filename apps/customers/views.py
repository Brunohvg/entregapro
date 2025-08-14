from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

from .models import Customer, Address
from apps.customers.forms import CustomerForm, AddressForm
from apps.customers.utils.customers import get_address_by_customer


# ===========================
# List e Detail Views
# ===========================

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        qs = Customer.objects.all().order_by('-created_at')
        if query:
            qs = qs.filter(
                Q(full_name__icontains=query) |
                Q(nickname__icontains=query) |
                Q(document__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            ).order_by('-created_at')
        return qs


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'


# ===========================
# Create & Update Customer Views
# ===========================

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'customers/hx/customer_createad_form_hx.html'
    fields = ['full_name', 'nickname', 'document', 'email', 'phone', 'observations']
    context_object_name = 'customer'

    def get_success_url(self):
        return reverse_lazy('customers:customer_list')

    def form_valid(self, form):
        self.object = form.save()
        response = HttpResponse(status=204)  # No Content
        response['HX-Redirect'] = self.get_success_url()
        return response


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/hx/customer_update_form_hx.html'
    context_object_name = 'customer'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = self.get_success_url()
        return response


# ===========================
# Address Views
# ===========================

class CustomerAdressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'customers/teste.html'
    context_object_name = 'address'

    def get_object(self, queryset=None):
        customer_id = self.kwargs.get("pk")
        return get_address_by_customer(customer_id=customer_id)

    def get_success_url(self):
        # Redireciona para o detalhe do cliente dono do endereço
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.customer.pk})

    def form_valid(self, form):
        self.object = form.save()
        response = HttpResponse(status=204)
        response['HX-Redirect'] = self.get_success_url()
        return response


# ===========================
# Function-based view para criar endereço com HTMX
# ===========================

def create_address_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = AddressForm(request.POST)
        street = request.POST.get('street')
        number = request.POST.get('number')
        # Verifica se já existe um endereço com esse CEP para esse cliente
        if Address.objects.filter(customer=customer, street=street).exists() or Address.objects.filter(customer=customer, number=number).exists():
            # Retorna uma mensagem de erro ou renderiza o formulário com aviso
            form.add_error('street', 'Este endereço já está cadastrado para este cliente.')
            return render(
                request,
                'customers/hx/form_address.html',
                {'form_address': form, 'customer': customer}
            )

        if form.is_valid():
            address = form.save(commit=False)
            address.customer = customer
            address.save()

            # Redirecionamento via HTMX
            response = HttpResponse()
            response['HX-Redirect'] = f'/customers/{customer.pk}/'
            return response
    else:
        form = AddressForm()

    return render(
        request,
        'customers/hx/form_address.html',
        {'form_address': form, 'customer': customer}
    )
