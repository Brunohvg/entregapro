# your_project/your_project/urls.py

from django.contrib import admin
from django.urls import path, include  # Importe 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),  # Inclui as URLs da aplicação 'accounts'
    path('orders/', include('apps.orders.urls')), # Inclui as URLs da aplicação 'orders'
    path('dashboard/', include('apps.dashboard.urls')), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)