from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from usuarios.models import Usuario
# Renomeie a função de login do Django para evitar conflito
from django.contrib.auth import authenticate, login as auth_login

from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.messages import constants


# nossas funções
def index(request):
    return render(request, 'bases/index.html')


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')

    elif request.method == "POST":
        print("📌 Dados recebidos no formulário:", request.POST)  # 🔥 Debug

        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Cadastro realizado com sucesso! Você já pode fazer login.")
            return redirect("login")
        else:
            messages.error(request, "Erro no formulário. Verifique os campos.")

    else:
        form = RegistrationForm()

    return render(request, "usuarios/cadastro.html", {"form": form})


def logar(request):
    if request.method == 'GET':
        return render(request, 'usuarios/login.html')

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return render(request,'carros/carros.html')
        else:
            messages.add_message(request, constants.ERROR,
                                 "usuario ou senha invalidos")
            return redirect("login")


def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta")
    return redirect("login")
