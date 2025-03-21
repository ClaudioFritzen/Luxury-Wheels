from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class CustomUsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('primeiro_nome', 'ultimo_nome', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'data_criacao', 'data_atualizacao')}),
    )

    # Configure os campos de pesquisa e exibição
    list_display = ('username', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    # Adicionei list_filter corretamente configurado

    list_filter = ('is_active', 'is_staff', 'is_superuser')  # Agora 'is_staff' funcionará
    

