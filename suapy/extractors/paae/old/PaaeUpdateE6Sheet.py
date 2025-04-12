import pandas as pd
from suapy.extractors.paae.Alimentacao import Alimentacao
from suapy.extractors.paae.Banco import Banco
from suapy.extractors.paae.PaaeEdital6Extractor import AlimentacaoConfig, PaaeEdital6Extractor
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler


class PaaeUpdateE6Sheet(PaaeEdital6Extractor):
    def __init__(
        self,
        headless: bool = False,
        alimentacao_config: AlimentacaoConfig = None,
        arquivo_inscritos: str = "",
        arquivos_removidos: str = ""
    ):
        super().__init__(headless=headless)
        self.alimentacao_config = alimentacao_config
        self.arquivo_inscritos = arquivo_inscritos
        self.arquivos_removidos = arquivos_removidos

    def soma_total(self, dados: list[dict]) -> float:
        return sum(float(d.get("Total", 0)) for d in dados)

    def processar_aluno(self, aluno: dict) -> dict:
        """Processa um único aluno e retorna um dicionário com os dados atualizados."""
        matricula = int(aluno["Matrícula"])
        inscricao = int(aluno["Inscrição"])
        nome = aluno["Nome"]

        cpf, periodo = self.access_student_register(matricula)
        profile_info = self.access_student_profile(inscricao)
        banco, agencia, conta, operacao = Parser.extrair_dados_bancarios(
            profile_info)
        tipo_conta = Banco.tipo_de_conta(banco, operacao)

        dados_aluno = {
            "Inscrição": inscricao,
            "Matrícula": matricula,
            "Nome": nome,
            "Periodo": periodo,
            "CPF": cpf,
            "Banco": banco,
            "Agência": agencia,
            "No da Conta": conta,
            "Tipo de Conta": tipo_conta,
            "Op.": operacao,
        }

        if self.alimentacao_config:
            self.coletar_pagamento_alimentacao(dados_aluno, matricula, periodo)

        return dados_aluno

    def coletar_pagamento_alimentacao(self, dados_aluno: dict, matricula: int, periodo: str) -> None:
        """Calcula e adiciona o valor de alimentação, se aplicável."""
        pagamento = (self.alimentacao_config.data_inicio,
                     self.alimentacao_config.data_fim)
        valor = Alimentacao.calcular_pagamento(pagamento, periodo)

        if valor == 0:
            print(
                f"\t⚠️ ATENÇÃO: Valor do auxílio alimentação zerado para: {self.SUAP_MATRICULA(matricula)}")
        elif valor > 0:
            dados_aluno["Total"] = valor

    def montar_resumo(self, dados: list[dict]) -> pd.DataFrame:
        """Gera o DataFrame da aba de resumo."""
        total_valor = self.soma_total(dados)
        return pd.DataFrame([
            {"Tipo": "Alimentação", "Qtd. Alunos": len(
                dados), "Valor individual": Alimentacao.valor_unitario, "Valor total": total_valor},
            {"Tipo": "", "Valor individual": "", "Qtd. Alunos": "", "Valor total": ""},
            {"Tipo": "", "Valor individual": "", "Qtd. Alunos": "", "Valor total": ""},
            {"Tipo": "", "Valor individual": "", "Qtd. Alunos": "", "Valor total": total_valor},
        ])

    def exec(self) -> None:
        print("🔍 Atualizando dados PAAE")

        handler = PlanilhaHandler(self.arquivo_inscritos)
        dados_planilha = handler.ler_planilha(header=0, sheet_name=1)

        self.login()
        print(f"📊 Total de inscritos: {len(dados_planilha)}")

        lista_dados = []
        lista_sem_conta = []

        for i, aluno in enumerate(dados_planilha, 1):
            try:
                print(f"📥 Atualizando dados: {i} de {len(dados_planilha)}")
                dados_aluno = self.processar_aluno(aluno)
                lista_dados.append(dados_aluno)

                if not all([
                    dados_aluno.get("Banco"),
                    dados_aluno.get("Agência"),
                    dados_aluno.get("No da Conta"),
                    dados_aluno.get("Op.")
                ]):
                    lista_sem_conta.append(dados_aluno)

            except Exception as e:
                print(
                    f"❌ [Erro] Atualizando dados: {i} de {len(dados_planilha)} - Campos inválidos!")
                print(e)

        dados_por_abas = {
            "Resumo": self.montar_resumo(lista_dados),
            "Alunos": pd.DataFrame(lista_dados)
        }

        handler.salvar_planilha_por_abas(dados_por_abas, "Planilha_Edital_06")
        handler.salvar_planilha(
            lista_sem_conta, "Planilha_Edital_06_alunos_sem_conta")

    @staticmethod
    def main() -> None:
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/RelatóriosPAAE/Planilha_Edital_06.2024_fev_e_mar_2025_RETIFICADA.xlsx"

        config = AlimentacaoConfig(
            data_inicio="01/04/2025",
            data_fim="30/04/2025",
        )

        paae_bot = PaaeUpdateE6Sheet(
            headless=True,
            arquivo_inscritos=inscritos_path,
            alimentacao_config=config
        )
        paae_bot.exec()
