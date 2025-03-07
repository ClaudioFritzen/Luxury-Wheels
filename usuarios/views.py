from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_list_or_404
from django.views.decorators.csrf import csrf_exempt

import json
from usuarios.models import Usuario
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from .forms import RegistrationForm

def index(request):
    return HttpResponse("Hello World")


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)  # Recebe os dados do formulário, e os valida
        if form.is_valid():  # Verifica se o formulário é válido
            user = form.save(commit=False)  # Salva os dados no banco de dados
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(f"Usuário {user.username} cadastrado com sucesso")
            auth_login(request, user)  # Loga o usuário automaticamente após o registro

            return redirect('index')  # Redireciona para a página inicial
        else:
            print(form.errors)
            print(f"Formulário inválido")
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form}) 



def login(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Username ou senha inválidos.'})
    else:
        return render(request, 'usuarios/login.html')


