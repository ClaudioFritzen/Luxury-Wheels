from django.db import models
from django.contrib.auth.hashers import make_password

from usuarios.validators import validar_senha


class Usuario(models.Model):
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    password = models.CharField(max_length=128)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    # def
    def clean(self):
        # chama a função validar_senha
        validar_senha(self.password)

    def save(self, *args, **kwargs):

        self.full_clean()  # ✅ Garante que as validações são aplicadas antes de salvar

        # Evita recriptografar senha já criptografada
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
