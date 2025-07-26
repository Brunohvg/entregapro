# your_project/accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'  # Define um namespace para as URLs desta aplicação

urlpatterns = [
    path('login/', views.user_login, name='authentication_login'),
    path('register/', views.user_register, name='authentication_register'),
    path('logout/', views.user_logout, name='user_logout'),
    # Adicione outras URLs de autenticação aqui, como redefinição de senha
    # path('password_reset/', views.password_reset_view, name='password_reset'),
]