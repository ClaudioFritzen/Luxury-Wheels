from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('aluguel', 'stripe_id', 'status', 'valor', 'data')
    search_fields = ('stripe_id', 'aluguel__carro__marca', 'aluguel__usuario__username')
    list_filter = ('status', 'data')
