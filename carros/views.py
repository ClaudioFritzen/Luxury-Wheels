from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Carro, Aluguel
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def lista_carros(request):
    carros = Carro.objects.all()
    return render(request, "carros/carros.html", {"carros": carros})


@login_required
def alugar_carro(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)

    if request.method == "POST":
        data_inicio = request.POST.get("data_inicio")
        data_fim = request.POST.get("data_fim")

        # 🔹 Print para depuração no console
        print(f"Data Início Recebida: {data_inicio}")
        print(f"Data Fim Recebida: {data_fim}")

        if not data_inicio or not data_fim:
            messages.error(
                request, "Você deve selecionar as datas do aluguel.")
            return redirect("alugar_carro", carro_id=carro.id)

        # Convertendo para tipo date no formato correto
        try:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

            # 🔹 Print das datas convertidas para depuração
            print(f"Data Início Convertida: {data_inicio}")
            print(f"Data Fim Convertida: {data_fim}")
        except ValueError as e:
            # 🔹 Print do erro de conversão para depuração
            print(f"Erro ao converter datas: {e}")
            messages.error(
                request, "Formato de data inválido. Utilize o formato YYYY-MM-DD.")
            return redirect("alugar_carro", carro_id=carro.id)

        if data_inicio >= data_fim:
            messages.error(
                request, "A data de início deve ser antes da data de fim.")
            return redirect("alugar_carro", carro_id=carro.id)

        # Incluir o dia de início no cálculo
        dias = (data_fim - data_inicio).days + 1
        preco_total = dias * carro.preco_diaria

        # 🔹 Print do cálculo de dias e preço total para depuração
        print(f"Dias de Aluguel: {dias}")
        print(f"Preço Total: € {preco_total}")

        # Renderizando a página de confirmação com os parâmetros no contexto
        return render(request, "carros/confirmar_aluguel.html", {
            "carro": carro,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "preco_total": preco_total,
            "dias": dias
        })

    return render(request, "carros/alugar.html", {"carro": carro})


@login_required
def confirmar_aluguel(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    print(f"Carro encontrado: {carro}")

    if request.method == "POST":
        data_inicio_str = request.POST.get('data_inicio')
        data_fim_str = request.POST.get('data_fim')
        preco_total = request.POST.get('preco_total')

        print(
            f"Confirmar aluguel: Data Início Recebida (Confirmação): {data_inicio_str}")
        print(
            f"Confirmar aluguel: Data Fim Recebida (Confirmação): {data_fim_str}")
        print(
            f"Confirmar aluguel: Preço Total Recebido (Confirmação): {preco_total}")

        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            print("Chegou aqui 1 try")
            print(f"Data Início Convertida primeiro try: {data_inicio}")
            print(f"Data Fim Convertida: {data_fim}")
        except ValueError as e:
            print(f"Erro ao converter datas: {e}")
            messages.error(request, "Formato de data inválido.")
            return redirect("confirmar_aluguel", carro_id=carro.id)
        print("Esta fora do 1 try")

        try:
            print("Entrou no segundo try")
            with transaction.atomic():
                aluguel = Aluguel.objects.create(
                    usuario=request.user,
                    carro=carro,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    preco_total=preco_total,
                )
                print(f"Aluguel criado: {aluguel}")

                carro.disponibilidade = False
                carro.save()
                print(
                    f"Disponibilidade do carro atualizada: {carro.disponibilidade}")
        except Exception as e:
            print(f"Erro durante a transação: {e}")
            messages.error(request, f"Erro ao confirmar o aluguel: {e}")
            return redirect("confirmar_aluguel", carro_id=carro.id)

        messages.success(
            request, f"Aluguel confirmado! Total: € {float(preco_total):.2f}")
        return redirect("meus_alugueis")

    return render(request, "carros/confirmar_aluguel.html", {
        "carro": carro,
        "data_inicio": request.POST.get('data_inicio'),
        "data_fim": request.POST.get('data_fim'),
        "preco_total": request.POST.get('preco_total')
    })


@login_required
def meus_alugueis(request):

    usuario = request.user  # Obter o usuário autenticado
    alugueis_ativos = Aluguel.objects.filter(
        usuario=usuario, status="Confirmado").order_by("-data_inicio")
    alugueis_finalizados = Aluguel.objects.filter(status="finalizado")
    return render(request, "carros/meus_alugueis.html", {
        "alugueis_ativos": alugueis_ativos,
        "alugueis_finalizados": alugueis_finalizados,
        "username": usuario.username  # Passar o nome do usuário para o template
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

    if request.method == "GET":
        # renderizar o formulario para ele preencher
        return render(request, "carros/estender_prazo.html", {"aluguel": aluguel})

    if request.method == "POST":
        # obter as novas datas: (str)
        nova_data_fim = request.POST.get("nova_data_fim") 
        print(f"Data não convertida {nova_data_fim}")
        print(type(nova_data_fim))

        # validação temos que converter as data do tipo str para datatime
        if nova_data_fim:
            # conversao
            nova_data_fim_convert = datetime.strptime(nova_data_fim, "%Y-%m-%d").date()

            aluguel.data_fim = nova_data_fim_convert
            print(f"Print da data convertida{nova_data_fim_convert}")
            print(type(nova_data_fim_convert))
            aluguel.save()
            messages.success(
                request, f"O prazo do aluguel foi estendido para {aluguel.data_fim}")

        else:
            messages.error(request, "Por Favor! insira uma data valida")

        # nova validação verificar 
        return redirect("meus_alugueis")
