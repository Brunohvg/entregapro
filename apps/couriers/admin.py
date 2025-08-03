from django.contrib import admin
from .models import Courier

class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', )
    search_fields = ('name', 'phone', )

admin.site.register(Courier, CourierAdmin)