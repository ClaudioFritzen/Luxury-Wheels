from django.shortcuts import render
from carros.models import Aluguel, Carro 
from django.db.models import Sum, Count, F

from pagamentos.models import Transacao
from gerenciamento.grafico_pagamento import gerar_grafico_pagamento

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

    # Receita por categoria de veículo
    receita_por_categoria = Carro.objects.values('categoria').annotate(
        receita_total=Sum(F('aluguéis__preco_total'))
    )
    # Aluguéis ativos
    alugueis_ativos = Aluguel.objects.filter(status="Ativo").count()
    print(alugueis_ativos)

    # Veículos com status "Ativo"
    veiculos_status = list(Aluguel.objects.filter(status="Ativo").values(
    'carro__marca', 'carro__modelo', 'status'
))
    # Pagamentos pendentes
    pagamentos_pendentes = Transacao.objects.filter(status="pendente").count()

    # Pagamentos cancelados
    pagamentos_cancelados = Transacao.objects.filter(status="falha").count()

    # Pagamentos reembolsados
    pagamentos_reembolsados = Transacao.objects.filter(status="reembolsado").count()

    # Pagamentos concluídos (sucesso)
    pagamentos_concluidos = Transacao.objects.filter(status="sucesso").count()

    # Gráfico de pagamentos
    gerar_grafico_pagamento(pagamentos_pendentes, pagamentos_cancelados, pagamentos_reembolsados, pagamentos_concluidos)

    # Contexto para o template
    context = {
        'total_alugueis': total_alugueis,
        'receita_total': receita_total,
        'carros_populares': carros_populares,
        'alugueis_por_categoria': alugueis_por_categoria,
        'alugueis_ativos': alugueis_ativos,
        'receita_por_categoria': receita_por_categoria,
        'veiculos_status': veiculos_status,  # Atualizado para refletir o modelo correto
        'pagamentos_concluidos': pagamentos_concluidos,
        'pagamentos_pendentes': pagamentos_pendentes,
        'pagamentos_cancelados': pagamentos_cancelados,
        'pagamentos_reembolsados': pagamentos_reembolsados,
    }

    return render(request, 'gerenciamento/relatorios.html', context)
