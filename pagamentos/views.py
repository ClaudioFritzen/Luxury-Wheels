from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.conf import settings
import stripe
from carros.models import Aluguel
from django.contrib import messages
from .models import Transacao


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def criar_sessao_pagamento(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id=aluguel_id)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Aluguel de {aluguel.carro.marca} {aluguel.carro.modelo}',
                        },
                        'unit_amount': int(aluguel.carro.preco * 100), #transforma o valor em centavos
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/pagamentos/sucesso'),
            cancel_url=request.build_absolute_uri('/pagamentos/cancelado'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)


def sucesso(request):
    # Obtenha os dados relevantes do Stripe (ex.: ID da sessão ou transação)
    stripe_id = request.GET.get('session_id')  # Exemplo: você pode passar o ID pela URL ou outros métodos
    
    # Simule a consulta ao Stripe para obter informações (em produção use a API do Stripe para validação)
    aluguel = Aluguel.objects.filter(transacao__stripe_id=stripe_id).first()

    if aluguel:
        # Atualize o status do aluguel
        aluguel.status = "Ativo"
        aluguel.save()

        # Salve a transação no banco de dados
        Transacao.objects.create(
            aluguel=aluguel,
            stripe_id=stripe_id,
            status="sucesso",
            valor=aluguel.preco_total
        )

    messages.success(request, "Seu pagamento foi concluído com sucesso!")
    return redirect('meus_alugueis')


def cancelado(request):
    messages.error(request, "O pagamento foi cancelado.")
    return redirect('meus_alugueis')

# def webhook(request):
#     return render(request, 'pagamentos/webhook.html')
