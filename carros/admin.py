from django.contrib import admin
from .models import Carro, Aluguel
from gerenciamento.models import Inspecao
# Register your models here.

admin.site.register(Carro)

@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    list_display = ("usuario", "carro", "data_inicio", "data_fim", "preco_total", "status")
    list_filter = ("status", "data_inicio", "data_fim")
    search_fields = ("usuario__username", "carro__modelo")