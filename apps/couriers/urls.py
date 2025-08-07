from django.urls import path
from . import views

app_name = 'couriers'

urlpatterns = [
    path('create/', views.CourierCreateView.as_view(), name='courier_create'),
    # URL para a tela de detalhes
    #path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    # ... outras urls
    #path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    # path('<int:id>/update/', views.customer_update_view, name='customer_update'),
]