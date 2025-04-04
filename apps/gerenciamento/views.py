from django.shortcuts import render
from carros.models import Aluguel, Carro 
from gerenciamento.models import Inspecao
from django.db.models import Sum, Count, F

from pagamentos.models import Transacao
from gerenciamento.grafico_pagamento import gerar_grafico_pagamento
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from gerenciamento.forms import InspecaoForm
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required('gerenciamento.ver_relatorios', raise_exception=True)
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



def tem_permissao_inspecao(user):
    return user.has_perm("gerenciamento.pode_gerenciar_inspecoes", raise_exception=True)


@login_required
@permission_required("gerenciamento.pode_gerenciar_inspecoes", raise_exception=True)
def lista_inspecoes(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    inspecoes = carro.inspecoes.all()

    return render(request, 'gerenciamento/lista_inspecoes.html', {
        "carro": carro,
        "inspecoes": inspecoes
    })


@login_required
@permission_required("gerenciamento.pode_gerenciar_inspecoes", raise_exception=True)
def nova_inspecao(request, carro_id):

    carro = get_object_or_404(Carro, id=carro_id)

    if request.method == "POST":
        form = InspecaoForm(request.POST)
        if form.is_valid():
            inspecao = form.save(commit=False)
            inspecao.carro = carro
            inspecao.save()
            return redirect('lista_inspecoes', carro_id=carro.id)
    else:
        form = InspecaoForm()

    return render(request, 'gerenciamento/nova_inspecao.html', {
        'form': form,
        'carro': carro,
    })

@login_required
@permission_required("gerenciamento.pode_gerenciar_inspecoes", raise_exception=True)
def editar_inspecao(request, inspecao_id):
    inspecao = get_object_or_404(Inspecao, id=inspecao_id)  # Obtém a inspeção pelo ID

    if request.method == "POST":  # Se o método for POST, processar o formulário enviado
        form = InspecaoForm(request.POST, instance=inspecao)
        if form.is_valid():  # Verifica se os dados do formulário são válidos
            form.save()  # Salva as alterações no banco de dados
            return redirect("lista_inspecoes", carro_id=inspecao.carro.id)
    else:  # Se o método for GET, inicializar o formulário com os dados atuais
        form = InspecaoForm(instance=inspecao)

    return render(request, "gerenciamento/editar_inspecao.html", {
        "form": form,
        "inspecao": inspecao,
    })


@login_required
@permission_required("gerenciamento.pode_gerenciar_inspecoes", raise_exception=True)
def excluir_inspecao(request, inspecao_id):
    inspecao = get_object_or_404(Inspecao, id=inspecao_id)
    carro_id = inspecao.carro.id
    inspecao.delete()
    return redirect('lista_inspecoes', carro_id=carro_id)