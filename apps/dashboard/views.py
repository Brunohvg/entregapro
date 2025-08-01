# /apps/dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
import json

from apps.orders.models import Order, DeliveryStatus, TypeOrder, PaymentStatus
from apps.customers.models import Customer

@login_required
def dashboard(request):
    """
    View para a página principal da dashboard.
    Coleta e exibe estatísticas vitais sobre pedidos e clientes.
    """
    now = timezone.now()
    
    # --- Cards de Resumo ---
    total_revenue_month = Order.total_orders_month()
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()
    pending_delivery_count = Order.objects.filter(delivery_status=DeliveryStatus.PENDING).count()

    # --- NOVO: Cálculo do Ticket Médio do Mês ---
    # Filtra os pedidos pagos do mês atual
    paid_orders_month = Order.objects.filter(
        payment_status=PaymentStatus.PAID,
        created_at__year=now.year,
        created_at__month=now.month
    )
    # Calcula a média do 'total_amount' para esses pedidos
    average_ticket_month = paid_orders_month.aggregate(avg_ticket=Avg('total_amount'))['avg_ticket'] or 0.0

    # --- Tabela de Pedidos Recentes ---
    recent_orders = Order.objects.select_related('customer').all()[:5]

    # --- Dados para o Gráfico de Ganhos Mensais (Últimos 6 meses) ---
    today = timezone.now().date()
    sales_data = []
    months_labels = []

    for i in range(5, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
        next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
        monthly_sales = Order.objects.filter(
            created_at__gte=month_start, created_at__lt=next_month
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        sales_data.append(float(monthly_sales))
        months_labels.append(month_start.strftime("%b/%y"))
        
    # --- Melhores Clientes ---
    top_customers = Customer.objects.order_by('-spent_total')[:5]

    # --- Gráfico: Tipos de Pedido (Whatsapp vs Correios) ---
    order_type_data = Order.objects.values('type_order').annotate(count=Count('id')).order_by()
    order_type_labels = [dict(TypeOrder.choices).get(item['type_order'], 'N/A') for item in order_type_data]
    order_type_series = [item['count'] for item in order_type_data]

    # --- Gráfico: Status de Entrega ---
    delivery_status_data = Order.objects.values('delivery_status').annotate(count=Count('id')).order_by()
    delivery_status_labels = [dict(DeliveryStatus.choices).get(item['delivery_status'], 'N/A') for item in delivery_status_data]
    delivery_status_series = [item['count'] for item in delivery_status_data]

    # --- Desempenho Geográfico (Top 5 Cidades por Faturamento) ---
    top_cities_data = Order.objects.filter(
        payment_status=PaymentStatus.PAID,
        customer__addresses__is_primary=True
    ).values(
        'customer__addresses__city'
    ).annotate(
        total_revenue=Sum('total_amount')
    ).order_by('-total_revenue').exclude(customer__addresses__city__isnull=True)[:5]

    city_labels = [item['customer__addresses__city'] for item in top_cities_data]
    city_series = [float(item['total_revenue']) for item in top_cities_data]

    context = {
        'total_revenue_month': total_revenue_month,
        'average_ticket_month': average_ticket_month, # NOVO
        'total_orders': total_orders,
        'total_customers': total_customers,
        'pending_delivery_count': pending_delivery_count,
        'recent_orders': recent_orders,
        'top_customers': top_customers,
        'sales_data': json.dumps(sales_data),
        'months_labels': json.dumps(months_labels),
        'order_type_labels': json.dumps(order_type_labels),
        'order_type_series': json.dumps(order_type_series),
        'delivery_status_labels': json.dumps(delivery_status_labels),
        'delivery_status_series': json.dumps(delivery_status_series),
        'city_labels': json.dumps(city_labels),
        'city_series': json.dumps(city_series),
        'segment': 'dashboard'
    }
    
    return render(request, 'dashboard/dashboard.html', context)
