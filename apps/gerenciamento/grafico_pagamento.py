import matplotlib.pyplot as plt

def gerar_grafico_pagamento(pagamentos_pendentes, pagamentos_cancelados, pagamentos_reembolsados, pagamentos_concluidos):
    # Dados de pagamentos
    labels = ['Pendente', 'Cancelado', 'Reembolsado', 'Concluído']
    counts = [pagamentos_pendentes, pagamentos_cancelados, pagamentos_reembolsados, pagamentos_concluidos]

    # Garantir que há dados para criar o gráfico
    total = sum(counts)
    if total == 0:
        print("Nenhum dado disponível para criar o gráfico.")
        return

    # Calcular porcentagens
    percentages = [(count / total) * 100 for count in counts]

    # Criar o gráfico de pizza
    fig, ax = plt.subplots()
    ax.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax.axis('equal')  # Para deixar o gráfico circular

    # Título e salvamento
    plt.title("Distribuição de Pagamentos por Status")
    plt.savefig('templates/static/gerenciamento/images/grafico_pizza.png')  # Salvar como imagem
    #plt.show() ## remover ou fechar
    #plt.close()  # Fechar a figura para liberar memória

# Exemplo de uso
if __name__ == "__main__":
    # Passe os dados de exemplo ou dados reais aqui
    pagamentos_pendentes = 5
    pagamentos_cancelados = 3
    pagamentos_reembolsados = 7
    pagamentos_concluidos = 10

    gerar_grafico_pagamento(pagamentos_pendentes, pagamentos_cancelados, pagamentos_reembolsados, pagamentos_concluidos)
