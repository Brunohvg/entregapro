# your_project/accounts/urls.py

from django.urls import path
from . import views

app_name = 'orders'  # Define um namespace para as URLs desta aplicação

urlpatterns = [
    path('list/', views.order_list, name='order_list'),

]