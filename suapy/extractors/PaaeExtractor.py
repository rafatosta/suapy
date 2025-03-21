from suapy.services.Banco import Banco
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler
from suapy.webdrive.SuapWebDrive import SuapWebDrive
from selenium.webdriver.common.by import By

import pandas as pd


class PaaeExtractor(SuapWebDrive):

    def __init__(self, headless=False):
        super().__init__(headless=headless)

    def SUAP_INSCRICAO(self, inscricao):
        return f"https://suap.ifba.edu.br/ae/visualizarinscricaoae/{inscricao}/"

    def SUAP_MATRICULA(self, matricula):
        return f"https://suap.ifba.edu.br/edu/aluno/{matricula}/"

    def access_student_profile(self, profile_id):
        self.load_page(self.SUAP_INSCRICAO(profile_id))

        element = self.find_element(
            By.XPATH, '//*[@id="content"]/div[3]/div[1]/div/table/tbody/tr[9]/td[2]')
        return element.text

    def access_student_register(self, register_id):
        try:
            self.load_page(self.SUAP_MATRICULA(register_id))

            cpf = self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[3]/td[2]')
            periodo = self.find_element(
                By.XPATH, '//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[4]/td[2]')

            return cpf.text, periodo.text
        except Exception as e:
            print(
                f"Erro ao tentar acessar registro do estudante ({self.SUAP_MATRICULA(register_id)}): \n\t{e}")
            return "", ""

    def exec(self):
        print("Coletando dados PAAE - Sem alimentação")
        self.login()

        alunos_inscritos = '/home/tosta/Documentos/GitHub/gerenciador-paae/report.xls'

        handler = PlanilhaHandler(alunos_inscritos)
        dados = handler.ler_planilha(header=1)
        print("Total de inscritos:", len(dados))

        lista_dados = []
        lista_sem_conta = []

        for i, aluno in enumerate(dados, 1):
            print(f"Coletando dados: {i} de {len(dados)}")

            nome_principal, nome_secundario, matricula = Parser.extrair_nome_e_matricula(
                aluno['Nome'])
            nome_secundario = f"({nome_secundario})" if nome_secundario else ""

            cpf, periodo = self.access_student_register(matricula)
            profile_info = self.access_student_profile(
                aluno['Numero da Inscrição'])
            banco, agencia, conta, operacao = Parser.extrair_dados_bancarios(
                profile_info)
            tipo_conta = Banco.tipo_de_conta(banco, operacao)

            dados_aluno = {
                'Inscrição': aluno['Numero da Inscrição'],
                'Matrícula': matricula,
                'Nome': f"{nome_principal} {nome_secundario}",
                'Periodo': periodo,
                'CPF': cpf,
                'Banco': banco,
                'Agência': agencia,
                'No da Conta': conta,
                'Tipo de Conta': tipo_conta,
                'Op.': operacao,
            }
            lista_dados.append(dados_aluno)

            if not (banco and agencia and conta and operacao):
                lista_sem_conta.append(dados_aluno)

        df = pd.DataFrame(lista_dados)
        df_sem_conta = pd.DataFrame(lista_sem_conta)

        df.to_excel('dados_alunos.xlsx', index=False)
        df_sem_conta.to_excel('dados_alunos_sem_conta.xlsx', index=False)

        print("Arquivo Excel salvo com sucesso!")
        self.close()
