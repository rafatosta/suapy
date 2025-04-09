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

    def ler_planilha(self, header=0, sheet_name=0) -> list:
        """
        Lê a planilha e armazena os dados em um DataFrame.
        Retorna os dados como uma lista de dicionários (orient='records').
        """
        try:
            self.dados_df = pd.read_excel(
                self.caminho_arquivo, header=header, sheet_name=sheet_name)
            print(
                f"✅ Planilha carregada com sucesso. Aba selecionada: {sheet_name}")
            return self.converter_para_dicionario_records()
        except FileNotFoundError:
            print(
                f"❌ Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
        except ValueError as e:
            print(f"❌ Erro: Aba '{sheet_name}' não encontrada. {e}")
        except Exception as e:
            print(f"❌ Erro ao ler a planilha: {e}")

    def converter_para_dicionario_records(self):
        """Converte o DataFrame para uma lista de dicionários (orient='records')."""
        try:
            if self.dados_df is not None:
                print("🔄 Conversão para dicionário (records) realizada com sucesso.")
                return self.dados_df.to_dict(orient="records")
            else:
                raise Exception(
                    "⚠️ Você precisa carregar a planilha primeiro.")
        except Exception as e:
            print(f"❌ Erro ao converter para dicionário (records): {e}")

    def salvar_planilha(self, dados, nome_arquivo, colunas_finais=None):
        """
        Salva os dados em um arquivo Excel dentro da pasta 'Relatórios',
        ajustando automaticamente a largura das colunas.
        """
        try:
            if not dados:
                raise ValueError("⚠️ Nenhum dado para salvar.")
            
            df = pd.DataFrame(dados)

            if colunas_finais:
                df = df[colunas_finais]


            # Formatar nome do arquivo com data e hora
            timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M")
            caminho_completo = os.path.join(
                self.pasta_relatorios, f"{nome_arquivo}_{timestamp}.xlsx"
            )

            with pd.ExcelWriter(caminho_completo, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Planilha')

                # Ajustar a largura das colunas
                workbook = writer.book
                worksheet = writer.sheets['Planilha']

                for idx, col in enumerate(df.columns):
                    col_width = max(
                        df[col].astype(str).map(len).max(),
                        len(col)
                    ) + 2  # margem extra
                    worksheet.set_column(idx, idx, col_width)

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

    def salvar_planilha_por_abas(self, data_dict, nome_arquivo):
        """
        Salva um dicionário de DataFrames em um arquivo Excel, onde cada chave do dicionário
        representa o nome da aba e o valor é um DataFrame correspondente, ajustando a largura das colunas.
        """
        try:
            # Formatar nome do arquivo com data e hora
            timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M")
            caminho_completo = os.path.join(
                self.pasta_relatorios, f"{nome_arquivo}_{timestamp}.xlsx"
            )
            with pd.ExcelWriter(caminho_completo, engine='xlsxwriter') as writer:
                for sheet_name, df in data_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

                    # Ajuste das larguras das colunas
                    workbook = writer.book
                    worksheet = writer.sheets[sheet_name]

                    for idx, col in enumerate(df.columns):
                        # Obtém o tamanho máximo entre o nome da coluna e os valores da coluna
                        col_width = max(
                            df[col].astype(str).map(len).max(),
                            len(col)
                        ) + 2  # Adiciona margem
                        worksheet.set_column(idx, idx, col_width)

            print(f"✅ Planilha salva com sucesso em: {caminho_completo}")
        except Exception as e:
            print(f"❌ Erro ao salvar planilha por abas: {e}")

    def atualizar_planilha(self, novos_dados, sheet_name):
        """
        Atualiza os dados de uma aba específica da planilha existente.
        Salva a nova versão diretamente na pasta de relatórios.
        """
        try:
            if not novos_dados:
                raise ValueError("⚠️ Nenhum dado para atualizar.")

            # Caminho para salvar a nova planilha
            novo_caminho = os.path.join(
                self.pasta_relatorios, os.path.basename(self.caminho_arquivo))
            os.makedirs(self.pasta_relatorios, exist_ok=True)

            # Lê todas as abas existentes
            with pd.ExcelFile(self.caminho_arquivo) as xls:
                planilhas = {nome: pd.read_excel(
                    xls, sheet_name=nome) for nome in xls.sheet_names}

            # Atualiza apenas a aba específica
            planilhas[sheet_name] = pd.DataFrame(novos_dados)

            # Salva todas as abas no novo arquivo Excel
            self.salvar_planilha_por_abas(
                planilhas, os.path.basename(self.caminho_arquivo))

            print(
                f"✅ Aba '{sheet_name}' atualizada com sucesso em '{novo_caminho}'.")

        except FileNotFoundError:
            print(
                f"❌ Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
        except KeyError:
            print(f"❌ Erro: A aba '{sheet_name}' não existe na planilha.")
        except Exception as e:
            print(f"❌ Erro ao atualizar a planilha: {e}")
