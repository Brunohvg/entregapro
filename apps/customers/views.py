from django.views.generic import ListView, DetailView
from .models import Customer
from django.db.models import Q

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
