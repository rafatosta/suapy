import re


class Parser:

    @staticmethod
    def extrair_nome_e_matricula(string):
        "Exemplo: Fulano de tal (12345612)"

        # Expressão regular para capturar nome e matrícula
        pattern = r"([A-Za-zÀ-ÖØ-öø-ÿ\s]+)\s*(?:\(([A-Za-zÀ-ÖØ-öø-ÿ\s]+)\))?\s*\((\d+)\)"

        # Aplicando o regex
        match = re.match(pattern, string)

        # Se houver correspondência, retornamos os grupos (nome principal, nome secundário e matrícula)
        if match:
            nome_principal = match.group(1).strip()
            nome_secundario = match.group(
                2).strip() if match.group(2) else None
            matricula = match.group(3).strip()
            return nome_principal, nome_secundario, matricula
        else:
            print(f"Não foi possível capturar nome e matrícula para: {string}")
            return None, None, None

    @staticmethod
    def extrair_dados_bancarios(string):
        # Divide a string em linhas
        linhas = string.strip().split("\n")

        # Inicializa um dicionário para armazenar os dados
        dados_bancarios = {'Banco': None, 'Agência': None,
                           'Conta': None, 'Operação': None}

        # Processa as linhas
        for i, linha in enumerate(linhas):
            if "Banco:" in linha:
                # Captura o valor da linha seguinte
                dados_bancarios['Banco'] = linhas[i +
                                                  1].strip() if i + 1 < len(linhas) else None
            elif "Agência:" in linha:
                # Captura o valor da linha seguinte
                dados_bancarios['Agência'] = linhas[i +
                                                    1].strip() if i + 1 < len(linhas) else None
            elif "Conta:" in linha:
                # Captura o valor da linha seguinte
                dados_bancarios['Conta'] = linhas[i +
                                                  1].strip() if i + 1 < len(linhas) else None
            elif "Operação:" in linha:
                # Captura o valor da linha seguinte
                dados_bancarios['Operação'] = linhas[i +
                                                     1].strip() if i + 1 < len(linhas) else None

        return (dados_bancarios['Banco'],
                dados_bancarios['Agência'],
                dados_bancarios['Conta'],
                dados_bancarios['Operação'])
