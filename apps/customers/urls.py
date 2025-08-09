# Em seu customers/urls.py

from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('list/', views.CustomerListView.as_view(), name='customer_list'),
    # URL para a tela de detalhes
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    # ... outras urls
    path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('<int:pk>/address/update/', views.CustomerAdressUpdateView.as_view(), name='customer_address_update'),
]