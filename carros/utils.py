from datetime import date

def calcular_dias_aluguel(data_inicio, data_fim):
    """
    Calcula o total de dias do aluguel, incluindo o dia inicial.
    """
    if data_inicio > data_fim:
        raise ValueError("A data de início não pode ser posterior à data final.")
    
    dias = (data_fim - data_inicio).days + 1  # Inclui o dia inicial
    return dias
