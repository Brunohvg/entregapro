# your_project/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages # Importe messages para feedback ao usuário

def user_login(request):
    """
    View para lidar com o login de usuários.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo de volta, {username}!")
                # Redireciona para o dashboard após o login bem-sucedido
                return redirect('core:dashboard')
            else:
                messages.error(request, "Nome de usuário ou senha inválidos.")
        else:
            messages.error(request, "Erro no formulário de login. Por favor, verifique suas credenciais.")
    else:
        form = AuthenticationForm() # Formulário vazio para requisições GET

    # Renderiza o template de login. Certifique-se de que 'authentication-login.html'
    # está em accounts/templates/accounts/
    return render(request, 'accounts/authentication-login.html', {'form': form})

def user_register(request):
    """
    View para lidar com o registro de novos usuários.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Use UserCreationForm para registro básico
        if form.is_valid():
            user = form.save()
            login(request, user) # Faz o login do usuário automaticamente após o registro
            messages.success(request, f"Sua conta foi criada com sucesso, {user.username}!")
            # Redireciona para o dashboard após o registro bem-sucedido
            return redirect('core:dashboard')
        else:
            # Se o formulário não for válido, as mensagens de erro estarão no próprio formulário
            messages.error(request, "Erro ao registrar. Por favor, corrija os erros abaixo.")
    else:
        form = UserCreationForm() # Formulário vazio para requisições GET

    # Renderiza o template de registro. Certifique-se de que 'authentication-register.html'
    # está em accounts/templates/accounts/
    return render(request, 'accounts/authentication-register.html', {'form': form})

def user_logout(request):
    """
    View para lidar com o logout de usuários.
    """
    logout(request)
    messages.info(request, "Você foi desconectado com sucesso.")
    # Redireciona para a página de login após o logout
    return redirect('accounts:authentication_login')