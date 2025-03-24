from suapy.extractors.paae.Alimentacao import Alimentacao
from suapy.extractors.paae.Banco import Banco
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler
from suapy.webdrive.SuapWebDrive import SuapWebDrive
from selenium.webdriver.common.by import By

from dataclasses import dataclass


@dataclass
class AlimentacaoConfig:
    data_inicio: str = ""
    data_fim: str = ""


class PaaeExtractor(SuapWebDrive):
    """Classe responsável por extrair dados do SUAP relacionados ao PAAE."""

    def __init__(self, headless=False, alimentacao_config: AlimentacaoConfig = None, arquivo_inscritos="", arquivos_removidos=""):
        """Inicializa o WebDriver."""
        super().__init__(headless=headless)

        self.alimentacao_config = alimentacao_config

        self.arquivo_inscritos = arquivo_inscritos
        self.arquivos_removidos = arquivos_removidos

    def SUAP_INSCRICAO(self, inscricao):
        """Retorna a URL da inscrição do aluno no SUAP."""
        return f"https://suap.ifba.edu.br/ae/visualizarinscricaoae/{inscricao}/"

    def SUAP_MATRICULA(self, matricula):
        """Retorna a URL do perfil do aluno no SUAP."""
        return f"https://suap.ifba.edu.br/edu/aluno/{matricula}/"

    def access_student_profile(self, profile_id):
        """
        Acessa o perfil do estudante e extrai as informações bancárias.
        """
        try:
            self.load_page(self.SUAP_INSCRICAO(profile_id))
            return self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div[1]/div/table/tbody/tr[9]/td[2]'
            ).text
        except Exception as e:
            print(f"Erro ao acessar perfil do estudante ({profile_id}): {e}")
            return ""

    def access_student_register(self, register_id):
        """
        Acessa o registro acadêmico do estudante e retorna o CPF e período.
        """
        try:
            self.load_page(self.SUAP_MATRICULA(register_id))

            cpf = self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[3]/td[2]'
            ).text

            periodo = self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[4]/td[2]'
            ).text

            return cpf, periodo

        except Exception as e:
            print(f"Erro ao acessar registro acadêmico ({register_id}): {e}")
            return "", ""

    def remover_alunos(self, dados, dados_removidos):
        """Remove alunos da lista de inscritos com base no CPF."""
        # Criando conjunto de CPFs removidos para busca eficiente
        cpfs_removidos = {aluno["CPF"]
                          for aluno in dados_removidos if "CPF" in aluno}

        # Filtrando os alunos que não estão na lista de removidos
        dados_filtrados = [
            aluno for aluno in dados
            if aluno.get("CPF") not in cpfs_removidos
        ]

        print(f"📉 Alunos removidos: {len(dados) - len(dados_filtrados)}")
        return dados_filtrados

    def exec(self):
        """Executa a extração de dados dos alunos do PAAE e gera relatórios."""
        print("🔍 Coletando dados PAAE")
        self.login()

        # Lendo os dados da planilha dos Alunos Inscritos
        handler = PlanilhaHandler(self.arquivo_inscritos)
        dados = handler.ler_planilha(header=1)

        # Lendo os dados da planilha dos Alunos a serem Removidos
        handler = PlanilhaHandler(self.arquivos_removidos)
        dados_removidos = handler.ler_planilha(header=0)

        print(f"📊 Total de inscritos: {len(dados)}")
        print(
            f"📊 Total de inscritos a serem removidos: {len(dados_removidos)}")

        # Listas para armazenar os dados coletados
        lista_dados = []
        lista_sem_conta = []

        # Para o auxílio alimentação
        if self.alimentacao_config:
            pagamento = (self.alimentacao_config.data_inicio,
                        self.alimentacao_config.data_fim)

        # Iteração sobre cada aluno na planilha
        for i, aluno in enumerate(dados, 1):
            print(f"📥 Coletando dados: {i} de {len(dados)}")

            # Extração dos dados básicos do aluno
            nome_principal, nome_secundario, matricula = Parser.extrair_nome_e_matricula(
                aluno["Nome"])
            nome_secundario = f"({nome_secundario})" if nome_secundario else ""

            # Coletando informações do estudante no SUAP
            cpf, periodo = self.access_student_register(matricula)
            profile_info = self.access_student_profile(
                aluno["Numero da Inscrição"])

            # Extraindo dados bancários
            banco, agencia, conta, operacao = Parser.extrair_dados_bancarios(
                profile_info)
            tipo_conta = Banco.tipo_de_conta(banco, operacao)

            # Montando o dicionário com os dados do aluno
            dados_aluno = {
                "Inscrição": aluno["Numero da Inscrição"],
                "Matrícula": matricula,
                "Nome": f"{nome_principal} {nome_secundario}",
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
                    dados_aluno["Alimentação"] = valor

            lista_dados.append(dados_aluno)

            # Se os dados bancários estiverem incompletos, adiciona à lista de alunos sem conta
            if not (banco and agencia and conta and operacao):
                lista_sem_conta.append(dados_aluno)

        # Removendo alunos da lista
        lista_dados = self.remover_alunos(lista_dados, dados_removidos)

        handler.salvar_planilha(lista_dados, "PAAE:dados_alunos")
        handler.salvar_planilha(lista_sem_conta, "PAAE:dados_alunos_sem_conta")

        self.close()
