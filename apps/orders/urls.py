# your_project/accounts/urls.py

from django.urls import path
from apps.orders.views import OrderList

app_name = 'orders'  # Define um namespace para as URLs desta aplicação

urlpatterns = [
    path('list/', OrderList.as_view(), name='order_list'),

]