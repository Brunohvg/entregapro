from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Customer, Address
from django.db.models import Q
from apps.customers.forms import CustomerForm, AddressForm

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Customer.objects.filter(
                Q(full_name__icontains=query) |
                Q(nickname__icontains=query) |
                Q(document__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            ).order_by('-created_at')
        return Customer.objects.all().order_by('-created_at')


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customers/hx/customer_createad_form_hx.html'
    fields = ['full_name', 'nickname', 'document', 'email', 'phone', 'observations']
    message = "Cliente criado com sucesso!"


    def get_success_url(self):
        return reverse_lazy('customers:customer_list')

    def form_valid(self, form):
        # Salva o formulário
        self.object = form.save()
        # Retorna uma resposta vazia ou um fragmento simples,
        # e usa os cabeçalhos HTMX para instruir o navegador a redirecionar
        response = HttpResponse(status=204)  # 204 No Content é uma boa prática aqui
        response['HX-Redirect'] = self.get_success_url()
        return response

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    context_object_name = 'customer'
    template_name = 'customers/hx/customer_update_form_hx.html'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        response = HttpResponse(status=204)  # No Content
        response['HX-Redirect'] = self.get_success_url()
        return response
    
class CustomerAdressUpdateView(UpdateView):
    model = Customer
    form_class = AddressForm
    context_object_name = 'address'
    template_name = 'customers/teste.html'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        response = HttpResponse(status=204)  # No Content
        response['HX-Redirect'] = self.get_success_url()
        return response
