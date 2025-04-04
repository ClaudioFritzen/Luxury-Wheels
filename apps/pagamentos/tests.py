from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from pagamentos.models import Transacao
from carros.models import Aluguel, Carro
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import get_user_model

User = get_user_model()
class TestPagamentos(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(username="usuario_teste", password="senha_teste", email="testespagamento@emai.com" )
        carro = Carro.objects.create(marca="Nissan", modelo="Qasqai", preco_diaria=15, ano=2018)
        aluguel = Aluguel.objects.create(
            usuario=usuario,
            carro=carro,
            data_inicio=date(2025, 4, 1),
            data_fim=date(2025, 4, 7),
            preco_total=105.00
        )
        Transacao.objects.create(
            aluguel=aluguel,
            stripe_id="sessao_teste_123",
            status="sucesso",
            valor=aluguel.preco_total
        )
    
    def test_transacao_salva_corretamente(self):
        transacao = Transacao.objects.get(stripe_id="sessao_teste_123")
        self.assertEqual(transacao.valor, 105.00)
        self.assertEqual(transacao.status, "sucesso")
