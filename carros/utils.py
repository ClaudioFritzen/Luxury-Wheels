from datetime import date, datetime
import locale

def calcular_dias_aluguel(data_inicio, data_fim):
    """
    Calcula o total de dias do aluguel, incluindo o dia inicial.
    """
    if data_inicio > data_fim:
        raise ValueError("A data de início não pode ser posterior à data final.")
    
    dias = (data_fim - data_inicio).days + 1  # Inclui o dia inicial
    return dias

def parse_data(data_str):
    """
    Analisa diferentes formatos de data e retorna um objeto de data.
    Suporta meses em português e inglês.
    """
    # Define as localizações para português e inglês
    locais = ['pt_PT.UTF-8', 'en_US.UTF-8']

    # Formatos aceitos
    formatos = [
        "%Y-%m-%d",        # ISO padrão (ex.: 2025-03-25)
        "%d/%m/%Y",        # Português usual (ex.: 25/03/2025)
        "%B %d, %Y",       # Texto com mês completo (ex.: Março 25, 2025 ou April 1, 2025)
        "%b %d, %Y",       # Texto com mês abreviado (ex.: Mar 25, 2025 ou Apr 1, 2025)
        "%m/%d/%Y",        # Formato americano (ex.: 03/25/2025)
        "%d-%m-%Y",        # Europeu alternativo (ex.: 25-03-2025)
        "%d.%m.%Y",        # Com pontos (ex.: 25.03.2025)
    ]

    for local in locais:
        try:
            locale.setlocale(locale.LC_TIME, local)  # Define o idioma do mês
            for formato in formatos:
                try:
                    return datetime.strptime(data_str, formato).date()
                except ValueError:
                    continue  # Tenta o próximo formato
        except locale.Error:
            continue  # Ignora caso a localização não esteja disponível no sistema

    # Caso nenhum formato seja válido
    print(f"Erro ao analisar a data: {data_str}")
    raise ValueError("Formato de data inválido.")
