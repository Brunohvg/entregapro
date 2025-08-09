from django.urls import path
from . import views

app_name = 'orders'  # Define um namespace para as URLs desta aplicação

urlpatterns = [
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.OrderCreated.as_view(), name='order_created'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update/',views.OrderUpdateView.as_view(), name='order_update' ),
    path('<int:pk>/delete/',views.OrderDeleteView.as_view(), name='order_delete' ),
    path('gerar_pdf/<int:pk>/',views.generate_label_pdf, name='gerar_pdf' ),
]
