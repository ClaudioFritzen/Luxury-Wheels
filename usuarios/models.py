from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from usuarios.validators import validar_senha


class Usuario(models.Model):
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    password = models.CharField(max_length=128)  # 🔹 Senha criptografada terá no máximo 128 caracteres
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
