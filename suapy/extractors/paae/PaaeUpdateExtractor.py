from suapy.extractors.paae.PAAEBase import PAAEBase
from suapy.extractors.paae.services.Banco import Banco
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler


from dataclasses import dataclass


@dataclass
class AlimentacaoConfig:
    data_inicio: str = ""
    data_fim: str = ""


class PaaeUpdateExtractor(PAAEBase):
    """Classe responsável por extrair dados do SUAP relacionados ao PAAE."""

    def __init__(self, headless=False, alimentacao_config: AlimentacaoConfig = None, arquivo_inscritos="", arquivos_novos=""):
        """Inicializa o WebDriver."""
        super().__init__(headless=headless)

        self.alimentacao_config = alimentacao_config

        self.arquivo_inscritos = arquivo_inscritos
        self.arquivos_novos = arquivos_novos

    def get_aluno(self, matricula_aluno, dados):

        for aluno in dados:
            _, _, matricula = Parser.extrair_nome_e_matricula(
                aluno["Nome"])

            if str(matricula).strip() == str(matricula_aluno).strip():
                return aluno

        return None

    def get_dados_alunos(self, aluno):
        # Extração dos dados básicos do aluno
        nome_principal, nome_secundario, matricula = Parser.extrair_nome_e_matricula(
            aluno["Nome"])
        nome_secundario = f"({nome_secundario})" if nome_secundario else ""

        print(nome_principal, "-", matricula)

        # Coletando informações do estudante no SUAP
        student_data = self.access_student_register(matricula)

        profile_info = self.access_student_profile(
            aluno["Numero da Inscrição"])

        tipo_conta = Banco.tipo_de_conta(
            profile_info["banco"], profile_info["operacao"])

        # Montando o dicionário com os dados do aluno
        dados_aluno = {
            "Inscrição": aluno["Numero da Inscrição"],
            "Matrícula": matricula,
            "Nome": f"{nome_principal} {nome_secundario}",
            "Curso:": student_data["curso"],
            "Periodo": student_data["periodo"],
            "CPF": student_data["cpf"],
            "Banco": profile_info["banco"],
            "Agência": profile_info["agencia"],
            "No da Conta": profile_info["conta"],
            "Tipo de Conta": tipo_conta,
            "Op.": profile_info["operacao"],
        }

        return dados_aluno

    def exec(self):
        """Executa a extração de dados dos alunos do PAAE e gera relatórios."""
        print("🔍 Coletando dados PAAE")
        self.login()

        # Lendo os dados da planilha dos Alunos Inscritos
        handler = PlanilhaHandler(self.arquivo_inscritos)
        dados = handler.ler_planilha(header=1)

        # Lendo os dados da planilha dos Alunos a serem Removidos
        handler2 = PlanilhaHandler(self.arquivos_novos)
        dados_novos = handler2.ler_planilha(header=0)

        # Listas para armazenar os dados coletados
        lista_dados = []
        lista_sem_conta = []

        print(f"📊 Total de novos inscritos: {len(dados_novos)}")

        for i, aluno in enumerate(dados_novos, 1):
            print(f"📥 Coletando dados: {i} de {len(dados_novos)}")

            novo_aluno = self.get_aluno(aluno["Matrícula"], dados)

            dados_aluno = self.get_dados_alunos(novo_aluno)

            print(dados_aluno)

            lista_dados.append(dados_aluno)

            # Se os dados bancários estiverem incompletos, adiciona à lista de alunos sem conta
            if not (dados_aluno["Banco"] and dados_aluno["Agência"] and dados_aluno["No da Conta"] and dados_aluno["Op."]):
                lista_sem_conta.append(dados_aluno)

        handler.salvar_planilha(lista_dados, "DADOS-EDITAL10")
        handler.salvar_planilha(
            lista_sem_conta, "DADOS-EDITAL10:SEM-CONTA")

        self.close()

    @staticmethod
    def main():
        # Caminho do arquivo com os alunos inscritos
        alunos_inscritos = "/home/tosta/Documentos/GitHub/suapy/EDITAL11.xls"
        alunos_novos = "/home/tosta/Documentos/GitHub/suapy/NOVOSEDITAL11.xlsx"

        paae_bot = PaaeUpdateExtractor(
            headless=False,
            arquivo_inscritos=alunos_inscritos,
            arquivos_novos=alunos_novos
        )
        paae_bot.exec()
