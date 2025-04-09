import pandas as pd
from suapy.extractors.paae.PaaeEdital6Extractor import PaaeEdital6Extractor
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler


class PaaeParserEdital7BuildAlunos(PaaeEdital6Extractor):
    def __init__(
        self,
        headless: bool = False,
        arquivo_inscritos: str = "",
    ):
        super().__init__(headless=headless)
        self.arquivo_inscritos = arquivo_inscritos

    def getAlunoEdital(self, lista, aluno_matricula):
        for aluno in lista:

            n, m, matricula = Parser.extrair_nome_e_matricula(aluno["Nome"])
            if str(aluno_matricula).strip() == matricula.strip():
                return aluno

        return None

    def inserir_chave(self, d, chave, valor, posicao):
        itens = list(d.items())
        itens.insert(posicao, (chave, valor))
        return dict(itens)

    def exec(self):
        handler = PlanilhaHandler(self.arquivo_inscritos)
        dados = handler.ler_planilha()
        self.login()

        """
            Faltam: Inscrição e Período 
        """

        handler_edital6 = PlanilhaHandler(
            "/home/tosta/Documentos/GitHub/suapy/Editais/PAAE-Editais-Originais/edital_6.xls")
        handler_edital7 = PlanilhaHandler(
            "/home/tosta/Documentos/GitHub/suapy/Editais/PAAE-Editais-Originais/edital_7.xls")

        edital6 = handler_edital6.ler_planilha(header=1)
        edital7 = handler_edital7.ler_planilha(header=1)

        for i, aluno in enumerate(dados, 1):
            print(f"📥 Coletando dados: {i} de {len(dados)}")

            aluno_e6 = self.getAlunoEdital(edital6, aluno["Matrícula"])
            aluno_e7 = self.getAlunoEdital(edital7, aluno["Matrícula"])

            if aluno_e6:
                aluno["Inscrição Edital 6"] = aluno_e6["Numero da Inscrição"]

            if aluno_e7:
                aluno["Inscrição"] = aluno_e7["Numero da Inscrição"]

            # cpf, periodo = self.access_student_register(aluno["Matrícula"])

            # aluno["Período"] = periodo

        colunas_finais = [
            "Inscrição", "Inscrição Edital 6", "Matrícula", "Nome", "Período", "CPF",
            "Banco", "Agência", "Número da Conta", "Tipo de conta", "Op.",
            "Alimentação", "Moradia", "Transporte", "Estudo"
        ]

        handler.salvar_planilha(dados, "Planilha_Edital_07_Final",colunas_finais)
        self.close()

    @staticmethod
    def main() -> None:
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/Relatórios/Planilha_Edital_07_AtualCompilado_2025-04-09_14h33.xlsx"
        paae_bot = PaaeParserEdital7BuildAlunos(
            headless=True,
            arquivo_inscritos=inscritos_path,
        )
        paae_bot.exec()
