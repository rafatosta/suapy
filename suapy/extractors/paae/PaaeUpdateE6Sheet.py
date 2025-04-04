

from suapy.extractors.paae.Alimentacao import Alimentacao
from suapy.extractors.paae.Banco import Banco
from suapy.extractors.paae.PaaeEdital6Extractor import AlimentacaoConfig, PaaeEdital6Extractor
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler
import pandas as pd


class PaaeUpdateE6Sheet(PaaeEdital6Extractor):

    def __init__(self, headless=False, alimentacao_config: AlimentacaoConfig = None, arquivo_inscritos="", arquivos_removidos=""):
        """Inicializa o WebDriver."""
        super().__init__(headless=headless)

        self.alimentacao_config = alimentacao_config

        self.arquivo_inscritos = arquivo_inscritos
        self.arquivos_removidos = arquivos_removidos

    def soma_total(self, dados):
        soma = 0
        for d in dados:
            soma += float(d["Total"])

        return soma

    def exec(self):
        """Executa a atualização do dados dos alunos do PAAE."""

        print("🔍 Atualizando dados PAAE")

        # Lendo os dados da planilha dos Alunos Inscritos
        handler = PlanilhaHandler(self.arquivo_inscritos)
        dados = handler.ler_planilha(header=0, sheet_name=1)
        self.login()

        print(f"📊 Total de inscritos: {len(dados)}")

        # Listas para armazenar os dados coletados
        lista_dados = []
        lista_sem_conta = []

        # Para o auxílio alimentação
        if self.alimentacao_config:
            pagamento = (self.alimentacao_config.data_inicio,
                         self.alimentacao_config.data_fim)

        for i, aluno in enumerate(dados, 1):
            try:
                matricula = int(aluno["Matrícula"])
                inscricao = int(aluno["Inscrição"])
                print(
                    f"📥 Atualizando dados: {i} de {len(dados)}: {aluno["Nome"]} ({matricula}) - {inscricao}")

                # Coletando informações do estudante no SUAP
                cpf, periodo = self.access_student_register(matricula)
                profile_info = self.access_student_profile(inscricao)
                # Extraindo dados bancários
                banco, agencia, conta, operacao = Parser.extrair_dados_bancarios(
                    profile_info)

                tipo_conta = Banco.tipo_de_conta(banco, operacao)

                # Montando o dicionário com os dados do aluno
                dados_aluno = {
                    "Inscrição": inscricao,
                    "Matrícula": matricula,
                    "Nome": aluno["Nome"],
                    "Periodo": periodo,
                    "CPF": cpf,
                    "Banco": banco,
                    "Agência": agencia,
                    "No da Conta": conta,
                    "Tipo de Conta": tipo_conta,
                    "Op.": operacao,
                }

                # Condicional para calcular o valor de alimentação
                if self.alimentacao_config:
                    valor = Alimentacao.calcular_pagamento(pagamento, periodo)

                    # Se o valor for 0, exibe uma mensagem de aviso
                    if valor == 0:
                        print('\tATENÇÃO: Valor do auxílio alimentação zerado para:',
                              self.SUAP_MATRICULA(matricula))

                    # Adiciona "Alimentação" ao dicionário apenas se o valor for maior que 0
                    if valor > 0:
                        dados_aluno["Total"] = valor

                lista_dados.append(dados_aluno)

                # Se os dados bancários estiverem incompletos, adiciona à lista de alunos sem conta
                if not (banco and agencia and conta and operacao):
                    lista_sem_conta.append(dados_aluno)

            except Exception as es:
                print(
                    f"❌ [Erro] Atualizando dados: {i} de {len(dados)} - Campos inválidos!")
                print(es)

         # Exemplo de dados para múltiplas abas
        dados_por_abas = {
            "Resumo": pd.DataFrame([
                {"Tipo": "Alimentação", "Qtd. Alunos": len(
                    lista_dados), "Valor total": self.soma_total(lista_dados)},
                {"Tipo": "", "Qtd. Alunos": "", "Valor total": ""},
                {"Tipo": "", "Qtd. Alunos": "", "Valor total": ""},
                {"Tipo": "", "Qtd. Alunos": "",
                    "Valor total":  self.soma_total(lista_dados)},
            ]),
            "Alunos": pd.DataFrame(lista_dados)
        }

        # Salvando a planilha com várias abas
        handler.salvar_planilha_por_abas(dados_por_abas, "Planilha_Edital_06")

        #Salvando a planilha com dados bancários incompletos
        handler.salvar_planilha(lista_sem_conta, "Planilha_Edital_06_alunos_sem_conta")

    @staticmethod
    def main():
        # Caminho do arquivo com os alunos inscritos
        alunos_inscritos = "/home/tosta/Documentos/GitHub/suapy/RelatóriosPAAE/Planilha_Edital_06.2024_fev_e_mar_2025_RETIFICADA.xlsx"
        alunos_removidos = ""

        config = AlimentacaoConfig(
            data_inicio="01/04/2025",
            data_fim="30/04/2025",
        )

        paae_bot = PaaeUpdateE6Sheet(
            headless=True,
            arquivo_inscritos=alunos_inscritos,
            arquivos_removidos=alunos_removidos,
            alimentacao_config=config
        )
        paae_bot.exec()
