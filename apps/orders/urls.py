from django.urls import path
from apps.orders.views import OrderListView, OrderCreated, OrderDetailView, gerar_etiqueta_pdf, OrderUpdateView,TesteMensagemView

app_name = 'orders'  # Define um namespace para as URLs desta aplicação

urlpatterns = [
    path('list/', OrderListView.as_view(), name='order_list'),
    path('created/', OrderCreated.as_view(), name='order_created'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('gerar_pdf/<int:pk>/',gerar_etiqueta_pdf, name='gerar_pdf' ),
    path('<int:pk>/update/',OrderUpdateView.as_view(), name='order_update' ),
    path('teste-mensagem/', TesteMensagemView.as_view(), name='teste_mensagem'),



]
