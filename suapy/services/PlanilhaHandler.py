import os
import pandas as pd
from datetime import datetime


class PlanilhaHandler:
    """Classe para manipulação de planilhas usando pandas."""

    def __init__(self, caminho_arquivo):
        """Inicializa a classe com o caminho do arquivo."""
        self.caminho_arquivo = caminho_arquivo
        self.dados_df = None
        self.pasta_relatorios = "Relatórios"

        # Garante que a pasta de relatórios existe
        os.makedirs(self.pasta_relatorios, exist_ok=True)

    def ler_planilha(self, header=0) -> list:
        """
        Lê a planilha e armazena os dados em um DataFrame.
        Retorna os dados como uma lista de dicionários (orient='records').
        
        Parâmetros:
        - header (int): Índice da linha do cabeçalho.
        """
        try:
            self.dados_df = pd.read_excel(self.caminho_arquivo, header=header)
            print("✅ Planilha carregada com sucesso.")
            return self.converter_para_dicionario_records()
        except FileNotFoundError:
            print(f"❌ Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
        except Exception as e:
            print(f"❌ Erro ao ler a planilha: {e}")

    def converter_para_dicionario_records(self):
        """Converte o DataFrame para uma lista de dicionários (orient='records')."""
        try:
            if self.dados_df is not None:
                print("🔄 Conversão para dicionário (records) realizada com sucesso.")
                return self.dados_df.to_dict(orient="records")
            else:
                raise Exception("⚠️ Você precisa carregar a planilha primeiro.")
        except Exception as e:
            print(f"❌ Erro ao converter para dicionário (records): {e}")

    def salvar_planilha(self, dados, nome_arquivo):
        """
        Salva os dados em um arquivo Excel dentro da pasta 'Relatórios'.
        
        Parâmetros:
        - dados (list[dict]): Lista de dicionários com os dados a serem salvos.
        - nome_arquivo (str): Nome base do arquivo sem extensão.
        """
        try:
            if not dados:
                raise ValueError("⚠️ Nenhum dado para salvar.")

            df = pd.DataFrame(dados)

            # Formatar nome do arquivo com data e hora
            timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M")

            caminho_completo = os.path.join(
                self.pasta_relatorios, f"{nome_arquivo}_{timestamp}.xlsx"
            )

            df.to_excel(caminho_completo, index=False)
            print(f"✅ Planilha salva com sucesso em: {caminho_completo}")

        except Exception as e:
            print(f"❌ Erro ao salvar planilha: {e}")

    def imprimir_tabulado_records(self):
        """Imprime os dados no formato 'records' de forma tabulada."""
        try:
            dados_dict = self.converter_para_dicionario_records()
            if dados_dict:
                for i, linha in enumerate(dados_dict, 1):
                    print(f"Linha {i}:")
                    for chave, valor in linha.items():
                        print(f"\t{chave}: {valor}")
                print("📑 Impressão tabulada (records) realizada com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao imprimir tabulado (records): {e}")
