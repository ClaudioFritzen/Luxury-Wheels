from datetime import date
from gerenciamento.models import Inspecao
from carros.models import Carro

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nome_do_projeto.settings')
django.setup()

from datetime import date


def listar_veiculos_com_inspecao():
    hoje = date.today()
    veiculos_com_inspecao = Inspecao.objects.filter(data_proxima_inspecao_obrigatoria__gte=hoje)

    for veiculo in veiculos_com_inspecao:
        print(f"Veículo: {veiculo.nome}, Data de Inspeção: {veiculo.data_proxima_inspecao_obrigatoria}")

if __name__ == "__main__":
    listar_veiculos_com_inspecao()
