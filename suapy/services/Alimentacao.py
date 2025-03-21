from datetime import datetime, timedelta


class Alimentacao:
    regras = {
        '1º': {'dias_contados': [0, 2]},  # Segunda e Quarta
        '2º': {'dias_contados': [0, 2]},  # Segunda e Quarta
        '3º': {'dias_contados': [0]}       # Apenas Segunda
    }
    valor_unitario = 11.0

    @staticmethod    
    def calcular_pagamento(pagamento, periodo):
        # Convertendo as strings de data para objetos datetime
        data_inicio = datetime.strptime(pagamento[0], "%d/%m/%Y")
        data_fim = datetime.strptime(pagamento[1], "%d/%m/%Y")

        # Calculando a quantidade de dias entre as duas datas
        quantidade_dias = (data_fim - data_inicio).days + \
            1  # +1 para incluir a data final

        # Contando os dias relevantes
        quantidade_dias_relevantes = 0
        data_atual = data_inicio
        dias_contados = Alimentacao.regras.get(periodo, {}).get('dias_contados', []) #fallback

        while data_atual <= data_fim:
            if data_atual.weekday() in dias_contados:
                quantidade_dias_relevantes += 1
            data_atual += timedelta(days=1)

        # Calculando o valor do pagamento com a nova fórmula
        valor_pagamento = quantidade_dias_relevantes * Alimentacao.valor_unitario
        # return quantidade_dias, quantidade_dias_relevantes, valor_pagamento
        return valor_pagamento


""" # Exemplo de uso
pagamento = ("01/08/2024", "30/09/2024")
valor_unitario = 11.0  # Exemplo de valor unitário da alimentação
periodo = '3º'  # Pode ser '1º', '2º' ou '3º'

alimentacao = Alimentacao(pagamento, valor_unitario, periodo)
quantidade_dias, quantidade_dias_relevantes, valor_pagamento = alimentacao.calcular_pagamento()

# Exibindo os resultados
print(f"Quantidade total de dias no período: {quantidade_dias}")
print(f"Quantidade de dias relevantes: {quantidade_dias_relevantes}")
print(f"Valor do pagamento: R$ {valor_pagamento:.2f}") """
