from .models import Transacao
from carros.models import Aluguel
from django.contrib import messages
import stripe
from django.urls import reverse

def criar_sessao_stripe(aluguel, carro, custo_adicional, data_fim_atual, nova_data_fim_str, dias_adicionais, request):
    """Cria uma sessão de pagamento no Stripe."""
    success_url = f"{request.build_absolute_uri(reverse('pagamentos:sucesso'))}?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{request.build_absolute_uri(reverse('pagamentos:cancelado'))}?session_id={{CHECKOUT_SESSION_ID}}"
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'Extensão de aluguel de {carro.marca} {carro.modelo}',
                        'description': f"De {data_fim_atual} a {nova_data_fim_str} ({dias_adicionais} dias)",
                    },
                    'unit_amount': int(custo_adicional * 100),  # Em centavos
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            'aluguel_id': aluguel.id,
            'usuario': request.user.username,
        }
    )
    return checkout_session

def verificar_transacao_pendente(aluguel):
    #Verifica se existe uma transação pendente para um aluguel.
    transacao_pendente = aluguel.transacoes.filter(status="pendente").first()
    
    if transacao_pendente and transacao_pendente.stripe_id:
        try:
            # Checa o status do PaymentIntent no Stripe
            stripe_status = stripe.PaymentIntent.retrieve(transacao_pendente.stripe_id)
            if stripe_status["status"] == "succeeded":
                return False  # Transação já foi paga
        except stripe.error.StripeError as e:
            print(f"Erro ao verificar transação no Stripe: {str(e)}")
            return False  # Assuma que não está pendente em caso de erro
        
    return bool(transacao_pendente)  # Retorna True se a transação pendente existir

  
def calcular_custos(dias_adicionais, preco_diaria):
    """Calcula o custo total adicional."""
    return dias_adicionais * preco_diaria


def criar_transacao(aluguel, custo_adicional):
    """Cria uma nova transação para o aluguel."""
    nova_transacao = Transacao.objects.create(
        aluguel=aluguel,
        status="pendente",
        valor=custo_adicional,
        stripe_id="",
    )
    return nova_transacao
