class Banco:
    # Dicionário estático para armazenar os bancos e suas operações de poupança
    bancos_poupanca = {
        'CAIXA ECONÔMICA': ["013", "1288"],
        'BANCO DO BRASIL': ["51"],
        'BRADESCO': ["013"],
        'NUBANK': [],
        'INTER': ["51"],
        'PICPAY': [],
        'C6': [],
        'MERCADO PAGO': [],
        'NEXT': [],
        'ITAU': ["500"]
    }

    @staticmethod
    def tipo_de_conta(nome_banco, operacao):
        """Retorna o tipo de conta com base no banco e número da operação."""
        if nome_banco in Banco.bancos_poupanca:
            if operacao in Banco.bancos_poupanca[nome_banco]:
                return "Poupança"
            else:
                return "Corrente"
        else:
            return ""  # Banco não cadastrado
