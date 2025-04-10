from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.conf import settings
import stripe
from carros.models import Aluguel
from django.contrib import messages
from .models import Transacao
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt



stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
from django.urls import reverse


def sucesso(request):
    stripe_id = request.GET.get('session_id')
    print(f"stripe_id de sucesso {stripe_id}")

    transacao = Transacao.objects.filter(stripe_id=stripe_id).first()
    if not transacao:
        messages.error(request, "Não foi possível encontrar a transação.")
        return redirect('meus_alugueis')

    if transacao:
        # Atualize o status da transação
        transacao.status = "sucesso"
        transacao.save()

        # Atualize o status do aluguel e disponibilidade do carro
        aluguel = transacao.aluguel
        aluguel.status = "Ativo"
        aluguel.save()

        # Atualize a disponibilidade do carro associado
        carro = aluguel.carro
        carro.disponibilidade = False
        carro.save()
    print(f"Status do aluguel antes de salvar: {aluguel.status}")
    print(f"Disponibilidade do carro antes de salvar: {carro.disponibilidade}")


    messages.success(request, "Seu pagamento foi concluído com sucesso!")
    return redirect('meus_alugueis')



def cancelado(request):
    stripe_id = request.GET.get('session_id')
    print(f"stripe_id de cancelado {stripe_id}")

    transacao = Transacao.objects.filter(stripe_id=stripe_id).first()
    
    if transacao:
        transacao.status="falha"
        transacao.save()
    messages.error(request, "O pagamento foi cancelado.")
    return redirect('meus_alugueis')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        stripe_id = session['id']
        transacao = Transacao.objects.filter(stripe_id=stripe_id).first()
        if transacao:
            transacao.status = 'sucesso'
            transacao.save()

            # Atualizar o status do aluguel e a disponibilidade do carro
            aluguel = transacao.aluguel
            aluguel.status = "Ativo"
            aluguel.save()

            carro = aluguel.carro
            carro.disponibilidade = False
            carro.save()

    return JsonResponse({'status': 'success'})
