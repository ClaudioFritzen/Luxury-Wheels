from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Carro, Aluguel, Inspecao
from datetime import datetime, date
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InspecaoForm
from .utils import calcular_dias_aluguel, parse_data
from pagamentos.models import Transacao
from django.conf import settings
import stripe
from django.urls import reverse

from pagamentos.utils import criar_transacao, calcular_custos,criar_sessao_stripe,verificar_transacao_pendente
from django.db import transaction
from django.db.models import F
# Create your views here.


def lista_carros(request):
    # Recuperar valores dos filtros enviados pelo usuário
    filtro_transmissao = request.GET.get('transmissao')
    filtro_combustivel = request.GET.get('combustivel')
    filtro_categoria = request.GET.get('categoria')
    filtro_tipo_veiculos = request.GET.get('tipo_veiculos')
    filtro_qtd_pessoas = request.GET.get('qtd_pessoas')
    filtro_valor_diaria = request.GET.get('preco_diaria')

    # Iniciar a query base
    carros = Carro.objects.all()
    user_has_permission = request.user.has_perm(
        'carros.pode_gerenciar_inspecoes')

    # Aplicar os filtros dinamicamente
    if filtro_transmissao:
        carros = carros.filter(transmissao=filtro_transmissao)
    if filtro_combustivel:
        carros = carros.filter(combustivel=filtro_combustivel)
    if filtro_categoria:
        carros = carros.filter(categoria=filtro_categoria)
    if filtro_tipo_veiculos:
        carros = carros.filter(tipo_veiculos=filtro_tipo_veiculos)
    if filtro_qtd_pessoas:
        carros = carros.filter(qtd_pessoas=filtro_qtd_pessoas)

    # <!-- Filtro de valor da diária -->
    if filtro_valor_diaria:
        if "-" in filtro_valor_diaria:
            min_valor, max_valor = filtro_valor_diaria.split("-")
            carros = carros.filter(
                preco_diaria__gte=min_valor, preco_diaria__lte=max_valor)

        elif "+" in filtro_valor_diaria:
            min_valor = filtro_valor_diaria.replace("+", "")
            carros = carros.filter(preco_diaria__gte=min_valor)
    # Retornar o contexto com os carros filtrados
    return render(request, "carros/carros.html", {
        "carros": carros,
        "filtro_transmissao": filtro_transmissao,
        "filtro_combustivel": filtro_combustivel,
        "filtro_categoria": filtro_categoria,
        "filtro_tipo_veiculos": filtro_tipo_veiculos,
        "filtro_qtd_pessoas": filtro_qtd_pessoas,
        'user_has_permission': user_has_permission,
        'filtro_valor_diaria': filtro_valor_diaria,

    })


@login_required
def alugar_carro(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    aluguel = Aluguel.objects.filter(carro=carro, usuario=request.user).first()

    if request.method == "GET":
        return render(request, "carros/alugar.html", {"carro": carro})

    if request.method == "POST":
        data_inicio_str = request.POST.get("data_inicio")
        data_fim_str = request.POST.get("data_fim")

        # Debug das datas recebidas
        print(
            f"Datas recebidas pelo formulário: Início {data_inicio_str}, Fim {data_fim_str}")
        print(f"Tipo de data_inicio_str: {type(data_inicio_str)}")

        if not data_inicio_str or not data_fim_str:
            messages.error(request, "Por favor, preencha as datas do aluguel.")
            return redirect("alugar_carro", carro_id=carro.id)

        try:
            # Converter datas usando nossa função parse_data no utils.py
            data_inicio = parse_data(data_inicio_str)
            data_fim = parse_data(data_fim_str)
            print(
                f"Data início convertida: {data_inicio}, TIPO {type(data_inicio)}, Data fim convertida: {data_fim}, TIPO {type(data_fim)}")

            if data_inicio < date.today():
                messages.error(
                    request, "A data de início não pode estar no passado.")
                return redirect("alugar_carro", carro_id=carro.id)

            if data_fim < data_inicio:
                messages.error(
                    request, "A data de término deve ser posterior à data de início.")
                return redirect("alugar_carro", carro_id=carro.id)

            # Usando a funcao no utils.py para calcular os dias
            dias = calcular_dias_aluguel(data_inicio, data_fim)
            print(f"Dias calculados: {dias}")
            preco_total = carro.preco_diaria * dias

            return render(request, "carros/confirmar_aluguel.html", {
                "carro": carro,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "preco_total": preco_total,
                "dias": dias,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                'aluguel': aluguel
            })

        except ValueError as ve:
            messages.error(
                request, "Formato de data inválido. Use o formato YYYY-MM-DD.")
            print(f"Erro ao converter datas: {ve}")
            return redirect("alugar_carro", carro_id=carro.id)


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def confirmar_aluguel(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)

    if request.method == "POST":
        # pegamos os dados do formulario
        data_inicio_str = request.POST.get('data_inicio')
        data_fim_str = request.POST.get('data_fim')

        try:
            # usar o transaction atomic para garantir que todas as operações sejam executadas ou nenhuma
            with transaction.atomic():
                # Verificar se as dadas foram fornecidas
                if not data_inicio_str or not data_fim_str:
                    messages.error(
                        request, "Por favor, preencha os campos início e final.")
                    return redirect("alugar_carro", carro_id=carro.id)

                # Converter datas usando nossa função parse_data no utils.py
                data_inicio = parse_data(data_inicio_str)
                data_fim = parse_data(data_fim_str)
                print(
                    f"Data início convertida em confirmar aluguel: {data_inicio}, Data fim convertida em confirmar aluguel: {data_fim}")

                if data_inicio < datetime.today().date():
                    messages.error(
                        request, "A data de início não pode estar no passado.")
                    return redirect("alugar_carro", carro_id=carro.id)

                if data_fim <= data_inicio:
                    messages.error(
                        request, "A data de término deve ser posterior à data de início.")
                    return redirect("alugar_carro", carro_id=carro.id)

                # Verificar disponibilidade
                if not carro.disponibilidade:
                    messages.error(
                        request, "O carro selecionado não está disponível para aluguel.")
                    return redirect("carros")
                
                # Calcular dias e preço total usando a função do utils.py
                dias = calcular_dias_aluguel(data_inicio, data_fim)
                preco_total = carro.preco_diaria * dias


                # Criar aluguel 
                aluguel = Aluguel.objects.create(
                    usuario=request.user,
                    carro=carro,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    preco_total=preco_total
                )
                # atualiza a disponibilidade do carro
                carro.disponibilidade = False
                carro.save()

                # Criar a transação
                transacao = criar_transacao(aluguel, preco_total)

                # criar sessao de pagamento no stripe
                checkout_session=criar_sessao_stripe(aluguel, carro, preco_total, data_inicio, data_fim, dias, request)

                # Atualizar stripe_id na Transacao
                transacao.stripe_id = checkout_session.id
                transacao.save()

                # Redirecionar ao Stripe
                return redirect(checkout_session.url, )

        except ValueError as e:
            messages.error(
                request, "Formato de data inválido. Use o formato AAAA-MM-DD.")
            print(f"Erro: {e}")
            return redirect("alugar_carro", carro_id=carro.id)

        except Exception as e:
            messages.error(
                request, "Ocorreu um erro inesperado ao processar o aluguel.")
            print(f"Erro inesperado: {e}")
            return redirect("carros")

    return redirect("carros")


@login_required
def meus_alugueis(request):

    usuario = request.user  # Obter o usuário autenticado
    alugueis_ativos = Aluguel.objects.filter(
        usuario=usuario, status="Confirmado").order_by("-data_inicio")
    alugueis_finalizados = Aluguel.objects.filter(status="finalizado")
    alugueis_cancelados = Aluguel.objects.filter(status="cancelado")
    alugueis_ativos = Aluguel.objects.filter(usuario=usuario,
                                             status__in=["Confirmado", "Ativo"]).order_by("-data_inicio")

    # adicionar o dia de hoje
    today = now().date()
    return render(request, "carros/meus_alugueis.html", {
        "alugueis_ativos": alugueis_ativos,
        "alugueis_finalizados": alugueis_finalizados,
        "username": usuario.username,  # Passar o nome do usuário para o template
        "alugueis_cancelados": alugueis_cancelados,
        "today": today
    })

@login_required
def entregar_veiculo(request, aluguel_id):
    if request.method == "GET":
        return meus_alugueis(request)

    if request.method == "POST":
        # buscar o aluguel
        aluguel = get_object_or_404(Aluguel, id=aluguel_id)
        aluguel.status = "finalizado"
        aluguel.save()

        # alterar o campo de disponibilidade no Carro para true
        carro = aluguel.carro
        carro.disponibilidade = True
        carro.save()

        messages.success(
            request, f"O veiculo {aluguel.carro.marca} {aluguel.carro.modelo} foi entregue com sucesso e está disponivel novamente!")
    return redirect("meus_alugueis")

@login_required
def extender_prazo(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id=aluguel_id)
    carro = aluguel.carro

    if request.method == "POST":
        nova_data_fim_str = request.POST.get("nova_data_fim")

        try:
            # Converter nova_data_fim_str para datetime.date
            with transaction.atomic(): # Garantir que todas as operações sejam executadas ou nenhuma
                nova_data_fim = parse_data(nova_data_fim_str)
                data_fim_atual = aluguel.data_fim  # Presume que já seja datetime.date

                # Verificar se nova_data_fim é maior que data_fim_atual
                if nova_data_fim <= data_fim_atual:
                    messages.error(
                        request, "A nova data deve ser posterior à data atual.")
                    return redirect('meus_alugueis')

                dias_adicionais = calcular_dias_aluguel(data_fim_atual, nova_data_fim)
                custo_adicional = calcular_custos(dias_adicionais, carro.preco_diaria)
                
                # Verificando se ja existe uma transação pendente
                # Buscar qualquer transação vinculada ao aluguel
                transacao_existente = verificar_transacao_pendente(aluguel)
                print(
                    f"Transações encontradas: {Transacao.objects.filter(aluguel=aluguel).values()}")
                print(
                    f"Transação pendente: {Transacao.objects.filter(aluguel=aluguel, status='pendente').values()}")
                
                
                if transacao_existente:
                    # se a transação estiver pendente, exiba a mensagem de aviso
                    messages.warning(request, "Já existe uma transação pendente para este aluguel.")
                    return redirect('meus_alugueis')
                
                # Atualizar ou criar transação
                nova_transacao = criar_transacao(aluguel, custo_adicional)

                # Atualizar aluguel
                aluguel.data_fim = nova_data_fim
                aluguel.preco_total += custo_adicional
                aluguel.save()

                # Configurar o stripe
                checkout_session = criar_sessao_stripe(
                    aluguel, carro, custo_adicional, data_fim_atual, nova_data_fim_str, dias_adicionais, request
                )
                nova_transacao.stripe_id = checkout_session.id
                nova_transacao.save()
                
            # Redirecionar ao Stripe
            return redirect(checkout_session.url)
        
        except ValueError as ve:
            messages.error(
                request, "Formato de data inválido. Use o formato AAAA-MM-DD.")
            print(f"Erro ao converter datas: {ve}")
            return redirect("meus_alugueis")
        
        except stripe.error.StripeError as stripe_error:
            messages.error(
                request, "Ocorreu um erro ao conectar-se ao Stripe. Tente novamente.")
            print(f"Erro do Stripe: {stripe_error}")
            return redirect("meus_alugueis")
        
        except Exception as e:
            messages.error(
                request, "Ocorreu um erro inesperado ao processar a extensão do aluguel.")
            print(f"Erro inesperado: {e}")
            return redirect("meus_alugueis")

    return render(request, "carros/estender_prazo.html", {"aluguel": aluguel})


@login_required
def cancelar_reserva(request, aluguel_id):
    # buscar id
    aluguel = get_object_or_404(Aluguel, id=aluguel_id, usuario=request.user)

    # verificar se a reserva pode ser cancelada
    if aluguel.data_inicio <= now().date():
        messages.error(
            request, "Não é possivel cancelar uma reserva que já foi iniciada ou concluída.")
        return redirect("meus_alugueis")

    try:  # cancelar a reverva
        aluguel.status = "cancelado"
        aluguel.save()

        # Tornando o veiculo disponivel novamente
        carro = aluguel.carro
        carro.disponibilidade = True
        carro.save()
        messages.success(
            request, f" A reserva do veículo {carro.marca} {carro.modelo} foi cancelada com sucesso!")

    except Exception as e:
        # printar os erros
        print(e)
        messages.error(request, f"Erro ao tentar cancelar a reserva: {e}")
        return redirect("meus_alugueis")

    return redirect("meus_alugueis")


def tem_permissao_inspecao(user):
    return user.has_perm("carros.pode_gerenciar_inspecoes")


@login_required
def lista_inspecoes(request, carro_id):
    # Verifica se o usuário tem a permissão necessária
    if not tem_permissao_inspecao(request.user):
        # Retorna a página 403 personalizada
        return render(request, '403.html', status=403)

    carro = get_object_or_404(Carro, id=carro_id)
    inspecoes = carro.inspecoes.all()

    return render(request, 'carros/lista_inspecoes.html', {
        "carro": carro,
        "inspecoes": inspecoes
    })


@login_required
def nova_inspecao(request, carro_id):
    # Verifica se o usuário tem a permissão necessária
    if not tem_permissao_inspecao(request.user):
        # Retorna a página 403 personalizada
        return render(request, '403.html', status=403)

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

    return render(request, 'carros/nova_inspecao.html', {
        'form': form,
        'carro': carro,
    })
