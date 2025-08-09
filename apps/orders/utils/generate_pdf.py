from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from apps.orders.models import Order

def generate_pdf(request, pk):
    order = Order.objects.get(pk=pk)
    address = order.customer.addresses.first()  # acessa o primeiro endereço do cliente

    html_string = render_to_string("partials/order_label.html", {
        "order": order,
        "primary_address": address
    })

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    return HttpResponse(pdf, content_type="application/pdf")