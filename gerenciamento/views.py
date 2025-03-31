from django.shortcuts import render
from carros.models import Aluguel, Carro 
from django.db.models import Sum, Count 


""" # Create your views here.
def relatorios(request):
    # Total de alugueis
    total_alugueis = Aluguel.objects.count()

    # Receita total
    receita_total = Aluguel.objects.aggregate(Sum('preco_total'))['preco_total__sum'] 

    # Carros mais alugados
    carros_mais_alugados = Aluguel.objects.values('carro__marca', 'carro__modelo').annotate(
        total_alugueis=Count('id')
    ).order_by('-total_alugueis')[:5]  # Top 5 carros mais alugados


    # Alugueis por categoria
    alugueis_ativos = Aluguel.objects.filter(status="Ativo").count()

    # Receita por categoria de veiculo
    receita_por_categoria = Aluguel.objects.values('carro__categoria').annotate(
        receita=Sum('preco_total')
    ).order_by('-receita')  # Receita total por categoria

    context = {
        "total_alugueis": total_alugueis,
        "receita_total": receita_total,
        "carros_mais_alugados": carros_mais_alugados,
        "alugueis_ativos": alugueis_ativos,
        "receita_por_categoria": receita_por_categoria,
    }

    return render(request, 'gerenciamento/relatorios.html', context)
 """
from django.shortcuts import render
from django.db.models import Sum, Count, F
from carros.models import Carro, Aluguel

def relatorios(request):
    # Total de aluguéis
    total_alugueis = Aluguel.objects.count()

    # Receita total gerada
    receita_total = Aluguel.objects.aggregate(total=Sum('preco_total'))['total']

    # Carros mais alugados
    carros_populares = Aluguel.objects.values('carro__marca', 'carro__modelo').annotate(
        total_alugueis=Count('id')
    ).order_by('-total_alugueis')[:5]  # Top 5 mais alugados

    # Aluguéis por categoria de carro
    alugueis_por_categoria = Carro.objects.values('categoria').annotate(
        total_alugueis=Count('aluguéis')
    )

    # Aluguéis ativos
    alugueis_ativos = Aluguel.objects.filter(status="Ativo").count()

    # Receita por categoria de veículo
    receita_por_categoria = Carro.objects.values('categoria').annotate(
        receita_total=Sum(F('aluguéis__preco_total'))
    )

    context = {
        'total_alugueis': total_alugueis,
        'receita_total': receita_total,
        'carros_populares': carros_populares,
        'alugueis_por_categoria': alugueis_por_categoria,
        'alugueis_ativos': alugueis_ativos,
        'receita_por_categoria': receita_por_categoria,
    }

    return render(request, 'gerenciamento/relatorios.html', context)
