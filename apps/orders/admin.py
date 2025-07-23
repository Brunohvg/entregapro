from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_amount',  )
    search_fields = ('order_number', )

admin.site.register(Order, OrderAdmin)