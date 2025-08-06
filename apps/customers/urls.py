# Em seu customers/urls.py

from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('list/', views.CustomerListView.as_view(), name='customer_list'),
    # URL para a tela de detalhes
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    # ... outras urls
    # path('create/', views.customer_create_view, name='customer_create'),
    # path('<int:id>/update/', views.customer_update_view, name='customer_update'),
]