from datetime import timedelta
from django.utils.timezone import now

def get_veiculos_indisponiveis_por_manutencao(veiculos):
    """
    Retorna uma lista de dicionários contendo veículos indisponíveis por manutenção
    e os respectivos motivos.
    """
    hoje = now().date()
    um_ano_atras = hoje - timedelta(days=365)
    indisponiveis = []

    for carro in veiculos:
        for inspecao in carro.inspecoes.all():
            if inspecao.data_ultima_inspecao and inspecao.data_ultima_inspecao < um_ano_atras:
                indisponiveis.append({
                    "carro": carro,
                    "motivo": "Última inspeção ultrapassou 1 ano"
                })
                break
            elif inspecao.data_proxima_revisao and inspecao.data_proxima_revisao <= hoje:
                indisponiveis.append({
                    "carro": carro,
                    "motivo": "Próxima revisão atrasada"
                })
                break

    return indisponiveis


def get_proxima_revisao_a_expirar(veiculos, dias_expiracao=15):
    """
    Retorna uma lista de dicionários contendo veículos com revisões que estão prestes a expirar
    dentro do número de dias especificado.
    """
    hoje = now().date()
    limite = hoje + timedelta(days=dias_expiracao)
    revisao_a_expirar = []

    for carro in veiculos:
        for inspecao in carro.inspecoes.all():
            if inspecao.data_proxima_revisao and hoje <= inspecao.data_proxima_revisao <= limite:
                revisao_a_expirar.append({
                    "id": carro.id,
                    "marca": carro.marca,
                    "modelo": carro.modelo,
                    "data_proxima_revisao": inspecao.data_proxima_revisao
                })
                break
    return revisao_a_expirar

def get_veiculos_inspecao_obrigatoria_a_expirar(veiculos, dias=15):
    """
    Retorna uma lista de dicionários contendo veículos com próxima inspeção obrigatória
    a expirar dentro do prazo especificado (default: 15 dias).
    """
    hoje = now().date()
    limite = hoje + timedelta(days=dias)
    inspecao_a_expirar = []

    for carro in veiculos:
        for inspecao in carro.inspecoes.all():
            if inspecao.data_proxima_inspecao_obrigatoria and hoje <= inspecao.data_proxima_inspecao_obrigatoria <= limite:
                inspecao_a_expirar.append({
                    "id": carro.id,
                    "marca": carro.marca,
                    "modelo": carro.modelo,
                    "data_proxima_inspecao_obrigatoria": inspecao.data_proxima_inspecao_obrigatoria
                })
                break

    return inspecao_a_expirar