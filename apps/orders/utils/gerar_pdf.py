from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from apps.orders.models import Order

def gerar_etiqueta_pdf(request, order_id):
    order = Order.objects.get(pk=order_id)
    address = order.customer.address_set.first()
    
    html_string = render_to_string("orders/order_label.html", {
        "order": order,
        "primary_address": address
    })

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    return HttpResponse(pdf, content_type="application/pdf")
