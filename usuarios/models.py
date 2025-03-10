from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("O usuário deve ter um email válido")
        if not username:
            raise ValueError("O usuário deve ter um username")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)  # 🔹 Isso garante que a senha seja armazenada com hash
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):  # 🔹 Agora ele herda de AbstractBaseUser
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)  # 🔹 Permite login
    is_admin = models.BooleanField(default=False)  # 🔹 Para futuros admins

    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
