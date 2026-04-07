from suapy.extractors.paae.services.Alimentacao import Alimentacao
from suapy.extractors.paae.services.Banco import Banco
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler
from suapy.webdrive.SuapWebDrive import SuapWebDrive
from selenium.webdriver.common.by import By

from dataclasses import dataclass


@dataclass
class AlimentacaoConfig:
    data_inicio: str = ""
    data_fim: str = ""


class PaaeExtractorComAlimentacao(SuapWebDrive):
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
            print(self.SUAP_INSCRICAO(profile_id))
            self.load_page(self.SUAP_INSCRICAO(profile_id))
            return self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div[1]/div/table/tbody/tr[12]/td[2]'
            ).text
        except Exception as e:
            print(f"Erro ao acessar perfil do estudante ({profile_id}): {e}")
            return ""

    def access_student_register(self, register_id):
        """
        Acessa o registro acadêmico do estudante e retorna o CPF e período.
        """
        try:
            print(self.SUAP_MATRICULA(register_id))
            self.load_page(self.SUAP_MATRICULA(register_id))

            cpf = self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[3]/td[2]'
            ).text

            periodo = self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[4]/td[2]'
            ).text

            curso = self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[5]/td[2]'
            ).text

            return cpf, periodo, curso

        except Exception as e:
            print(f"Erro ao acessar registro acadêmico ({register_id}): {e}")
            return "", ""

    def coletar_pagamento_alimentacao(self, matricula: int, periodo: str) -> None:
        """Calcula e adiciona o valor de alimentação, se aplicável."""
        pagamento = (self.alimentacao_config.data_inicio,
                     self.alimentacao_config.data_fim)
        valor = Alimentacao.calcular_pagamento(pagamento, periodo)

        if valor == 0:
            print(
                f"\t⚠️ ATENÇÃO: Valor do auxílio alimentação zerado para: {self.SUAP_MATRICULA(matricula)}")
        return valor

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
        if dados_removidos:
            print(
                f"📊 Total de inscritos a serem removidos: {len(dados_removidos)}")

        # Listas para armazenar os dados coletados
        lista_dados = []
        lista_sem_conta = []

        # Iteração sobre cada aluno na planilha
        for i, aluno in enumerate(dados, 1):
            print(f"📥 Coletando dados: {i} de {len(dados)}")

            # Extração dos dados básicos do aluno
            nome_principal, nome_secundario, matricula = Parser.extrair_nome_e_matricula(
                aluno["Nome"])
            nome_secundario = f"({nome_secundario})" if nome_secundario else ""

            print(nome_principal, "-", matricula)

            # Coletando informações do estudante no SUAP
            cpf, periodo, curso = self.access_student_register(matricula)
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
                "Curso:": curso,
                "Periodo": periodo,
                "CPF": cpf,
                "Banco": banco,
                "Agência": agencia,
                "No da Conta": conta,
                "Tipo de Conta": tipo_conta,
                "Op.": operacao,
            }

            if self.alimentacao_config:
                dados_aluno["valor"] = self.coletar_pagamento_alimentacao(
                    matricula, periodo)

            lista_dados.append(dados_aluno)

            # Se os dados bancários estiverem incompletos, adiciona à lista de alunos sem conta
            if not (banco and agencia and conta and operacao):
                lista_sem_conta.append(dados_aluno)

        handler.salvar_planilha(lista_dados, "PAAE:Edital-11")
        handler.salvar_planilha(
            lista_sem_conta, "PAAE:Edital-11-sem_dados_bancarios")
        self.close()

    @staticmethod
    def main():
        # Caminho do arquivo com os alunos inscritos
        alunos_inscritos = "/home/tosta/Documentos/GitHub/suapy/report11.xls"

        config = AlimentacaoConfig(
            data_inicio="01/11/2025",
            data_fim="30/11/2025",
        )

        paae_bot = PaaeExtractorComAlimentacao(
            headless=True,
            arquivo_inscritos=alunos_inscritos,
            alimentacao_config=config
        )
        paae_bot.exec()
