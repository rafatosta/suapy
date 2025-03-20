import pandas as pd


class PlanilhaHandler:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.dados_df = None

    def ler_planilha(self, header=0) -> list:
        """Lê a planilha e armazena o DataFrame com tratamento de exceções.
        header-> aponta para a linha do cabeçalho da tabela.
        """
        try:
            self.dados_df = pd.read_excel(self.caminho_arquivo, header=header)
            print("Planilha carregada com sucesso.")
            return self.converter_para_dicionario_records()
        except FileNotFoundError:
            print(
                f"Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
        except Exception as e:
            print(f"Erro ao ler a planilha: {e}")

    def converter_para_dicionario_records(self):
        """Converte o DataFrame para uma lista de dicionários (orient='records')."""
        try:
            if self.dados_df is not None:
                print("Conversão para dicionário (records) realizada com sucesso.")
                return self.dados_df.to_dict(orient='records')
            else:
                raise Exception("Você precisa carregar a planilha primeiro.")
        except Exception as e:
            print(f"Erro ao converter para dicionário (records): {e}")

    def imprimir_tabulado_records(self):
        """Imprime os dados no formato orient='records' de forma tabulada."""
        try:
            dados_dict = self.converter_para_dicionario_records()
            if dados_dict:
                for i, linha in enumerate(dados_dict, 1):
                    print(f"Linha {i}:")
                    for chave, valor in linha.items():
                        print(f"\t{chave}: {valor}")
                print("Impressão tabulada (records) realizada com sucesso.")
        except Exception as e:
            print(f"Erro ao imprimir tabulado (records): {e}")
