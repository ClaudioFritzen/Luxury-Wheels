# usuarios/views.py
from django.contrib.auth import login
from django.http import HttpResponse
from .forms import RegistrationForm


from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from usuarios.models import Usuario
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from .forms import RegistrationForm

def index(request):
    return render(request, 'bases/index.html')


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


#### Criando a classe de testes

class UsuarioListView(View):
    def get(self, request):
        """Lista todos os usuarios"""
        usuarios = Usuario.objects.values("id", "primeiro_nome", "ultimo_nome", "email", "username" )
        return JsonResponse(list(usuarios), safe=False)
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        """Cria um novo usuario """
        data = json.loads(request.body)
        usuario = Usuario.objects.create(
            primeiro_nome=data["primeiro_nome"],
            ultimo_nome=data["ultimo_nome"],
            email=data["email"],
            username=data["username"],
            password=data["password"]
        )
        return JsonResponse({"id":usuario.id, "message":"Usuário criado com sucesso"}, status=201)
    

class UsuarioDetailView(View):
    def get(self, request, pk):
        # Obtem os detalhes de um salario
        usuario = get_list_or_404(Usuario, pk=pk)
        return JsonResponse({
            "id": usuario.id,
            "primeiro_nome": usuario.primeiro_nome,
            "ultimo_nome": usuario.ultimo_nome,
            "email": usuario.email,
            "username": usuario.username,
        })
    
    @method_decorator(csrf_exempt)
    def put(self, request, pk):
        # Atualiza um usuário
        usuario = get_list_or_404(usuario, pk=pk)
        data = json.loads(request.body)
        usuario.primeiro_nome = data.get("primeiro_nome", usuario.primeiro_nome)
        usuario.ultimo_nome = data.get("ultimo_nome", usuario.ultimo_nome)
        usuario.save()
        return JsonResponse({"message": "Usuario atualizado com suceso"})
    
    @method_decorator(csrf_exempt)
    def delete(self, request, pk):
        # Exclui um usuario
        usuario = get_list_or_404(Usuario, pk)
        usuario.delete()
        return JsonResponse({"message": "Usuário excluído com sucesso"}, status=204)