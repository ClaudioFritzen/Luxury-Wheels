from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
        user.is_superuser = True  # 🔹 Necessário para superusuários no Django Admin
        user.is_staff = True  # 🔹 Adicione essa linha!
        user.save(using=self._db)
        return user

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Usuario(AbstractBaseUser, PermissionsMixin):
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  # 🔹 Tem que ser um BooleanField
    is_admin = models.BooleanField(default=False)  

    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Admins têm todas as permissões
        if self.is_admin:
            return True
        # O PermissionsMixin verifica as permissões padrão
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        # Admins têm acesso total a módulos
        if self.is_admin:
            return True
        # O PermissionsMixin verifica os módulos
        return super().has_module_perms(app_label)

