from django.contrib import admin
from .models import Customer, Address
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'street', 'number', 'postal_code', )
    search_fields = ('postal_code', 'street', )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'document', 'email', 'spent_total', )
    search_fields = ('document', 'nickname', 'full_name', 'email', )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)