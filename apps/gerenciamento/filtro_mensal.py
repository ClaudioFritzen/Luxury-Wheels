from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime
from carros.models import Aluguel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


def filtrar_faturamento_por_mes(mes, ano):
    # Filtra os aluguéis pelo mês e ano selecionados
    alugueis_filtrados = Aluguel.objects.filter(
        data_inicio__month=mes,
        data_inicio__year=ano
    )

    # Calcula a receita total do período
    receita_total = alugueis_filtrados.aggregate(Sum('preco_total'))['preco_total__sum'] or 0

    return {
        'alugueis': alugueis_filtrados,
        'receita_total': receita_total
    }
