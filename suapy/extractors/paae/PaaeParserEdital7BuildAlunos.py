import pandas as pd
from suapy.extractors.paae.Banco import Banco
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

    def getDadosBancarios(self, inscricao):
        profile_info = self.access_student_profile(inscricao)

        # Extraindo dados bancários
        banco, agencia, conta, operacao = Parser.extrair_dados_bancarios(
            profile_info)
        tipo_conta = Banco.tipo_de_conta(banco, operacao)

        return banco, agencia, conta, operacao, tipo_conta

    def inserir_chave(self, d, chave, valor, posicao):
        itens = list(d.items())
        itens.insert(posicao, (chave, valor))
        return dict(itens)

    def compararDadosBancarios(self, inscricao_1, inscricao_2, getDadosBancarios):
        """
        Executa a busca de dados bancários apenas se a inscrição for válida (int).
        Se ambas forem válidas, compara os dados e retorna o que estiver completo.
        Se apenas uma for válida, retorna essa.
        Se nenhuma for válida, retorna campos nulos.

        Args:
            inscricao_1 (int | None): Número da inscrição (ex: aluno["Inscrição"])
            inscricao_2 (int | None): Número da inscrição (ex: aluno["Inscrição Edital 6"])
            getDadosBancarios (callable): Função que recebe uma inscrição e retorna os dados bancários

        Returns:
            dict: Contendo os dados obtidos, campos vazios e (se aplicável) diferenças
        """
        print(
            f"{inscricao_1} ({type(inscricao_1)}), {inscricao_2} ({type(inscricao_2)})")
        if not callable(getDadosBancarios):
            raise TypeError(
                "O parâmetro 'getDadosBancarios' precisa ser uma função.")

        campos = ["banco", "agencia", "conta", "operacao", "tipo_conta"]

        def obter_dados(inscricao):
            if not isinstance(inscricao, int):
                return None
            dados = getDadosBancarios(inscricao)
            if not isinstance(dados, (list, tuple)) or len(dados) != len(campos):
                raise ValueError(
                    f"A função getDadosBancarios deve retornar {len(campos)} valores.")
            return dict(zip(campos, dados))

        dados1 = obter_dados(inscricao_1)
        dados2 = obter_dados(inscricao_2)

        vazios_1 = {k: v for k, v in dados1.items() if not v} if dados1 else {}
        vazios_2 = {k: v for k, v in dados2.items() if not v} if dados2 else {}

        diferencas = {}
        if dados1 and dados2:
            diferencas = {k: (dados1[k], dados2[k])
                          for k in campos if dados1[k] != dados2[k]}
            if not vazios_1 and vazios_2:
                dados_preferido = dados1
            elif not vazios_2 and vazios_1:
                dados_preferido = dados2
            elif not vazios_1 and not vazios_2:
                dados_preferido = dados1  # arbitrário
            else:
                dados_preferido = None
        else:
            dados_preferido = dados1 or dados2

        return {
            "dados_inscricao": dados1,
            "dados_edital6": dados2,
            "vazios_inscricao": vazios_1,
            "vazios_edital6": vazios_2,
            "diferencas": diferencas,
            "dados_preferido": dados_preferido
        }

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

            aluno["Inscrição Edital 6"] = ""

            if aluno_e6:
                aluno["Inscrição Edital 6"] = aluno_e6["Numero da Inscrição"]

            if aluno_e7:
                aluno["Inscrição"] = aluno_e7["Numero da Inscrição"]

            # Atualiza período
            cpf, periodo = self.access_student_register(aluno["Matrícula"])
            aluno["Período"] = periodo

            # Atualiza dados bancários
            resultado = self.compararDadosBancarios(
                aluno.get("Inscrição", ""),
                aluno.get("Inscrição Edital 6", ""),
                self.getDadosBancarios
            )

            if resultado["dados_preferido"]:
                aluno["Banco"] = resultado["dados_preferido"].get("banco", "")
                aluno["Agência"] = resultado["dados_preferido"].get(
                    "agencia", "")
                aluno["Conta"] = resultado["dados_preferido"].get("conta", "")
                aluno["Operação"] = resultado["dados_preferido"].get(
                    "operacao", "")
                aluno["Tipo Conta"] = resultado["dados_preferido"].get(
                    "tipo_conta", "")

            """ if resultado["dados_preferido"]:
                print("Dados:", resultado["dados_preferido"]) """

        # Organiza as colunas da tabela
        colunas_finais = [
            "Inscrição", "Inscrição Edital 6", "Matrícula", "Nome", "Período", "CPF",
            "Banco", "Agência", "Número da Conta", "Tipo de conta", "Op.",
            "Alimentação", "Moradia", "Transporte", "Estudo"
        ]

        handler.salvar_planilha(
            dados, "Planilha_Edital_07_Final", colunas_finais)
        self.close()

    @staticmethod
    def main() -> None:
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/Relatórios/Planilha_Edital_07_AtualCompilado_2025-04-09_14h33.xlsx"
        paae_bot = PaaeParserEdital7BuildAlunos(
            headless=True,
            arquivo_inscritos=inscritos_path,
        )
        paae_bot.exec()
