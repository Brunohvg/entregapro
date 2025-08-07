from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Courier
from django.views.generic import CreateView




class CourierCreateView(CreateView):
    model = Courier
    fields = ['name', 'phone', 'document', 'is_active']
    template_name = 'couriers/hx/couriers_create_from.html'
    success_url = '/couriers/'  # Redireciona para a lista de couriers após a criação
    context_object_name = 'courier'


    def get_success_url(self):
        return reverse_lazy('couriers:courier_create')

    def form_valid(self, form):
        # Salva o formulário
        self.object = form.save()
        # Retorna uma resposta vazia ou um fragmento simples,
        # e usa os cabeçalhos HTMX para instruir o navegador a redirecionar
        response = HttpResponse(status=204)  # 204 No Content é uma boa prática aqui
        response['HX-Redirect'] = self.get_success_url()
        return response
    