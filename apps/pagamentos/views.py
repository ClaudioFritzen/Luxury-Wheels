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
    # Obtenha os dados relevantes do Stripe (ex.: ID da sessão ou transação)
    stripe_id = request.GET.get('session_id')  # Exemplo: você pode passar o ID pela URL ou outros métodos
    print(f"stripe_id de sucesso {stripe_id}")
    # busque a transação assicioada ao ID da sessao
    transacao = Transacao.objects.filter(stripe_id=stripe_id).first()
    if not transacao:
        messages.error(request, "Não foi possível encontrar a transação.")
        return redirect('meus_alugueis')

    if transacao:
        # Atualize o status da transação para "sucesso"
        transacao.status = "sucesso"
        transacao.save()

        # Atualize o status do aluguel relacionado à transação
        aluguel = transacao.aluguel
        aluguel.status = "Ativo"
        aluguel.save()


    #informando usuário que o pagamento foi concluído com sucesso
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

    return JsonResponse({'status': 'success'})
