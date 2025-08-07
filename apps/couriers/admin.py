from django.contrib import admin
from .models import Courier

class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone',  'is_active', 'document', 'created_at', 'updated_at',)
    search_fields = ('name', 'phone',  )

admin.site.register(Courier, CourierAdmin)