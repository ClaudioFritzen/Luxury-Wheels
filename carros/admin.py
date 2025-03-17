from django.contrib import admin
from .models import Carro, Inspecao, Aluguel
# Register your models here.

admin.site.register(Carro)
admin.site.register(Inspecao)


@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    list_display = ("usuario", "carro", "data_inicio", "data_fim", "preco_total", "status")
    list_filter = ("status", "data_inicio", "data_fim")
    search_fields = ("usuario__username", "carro__modelo")