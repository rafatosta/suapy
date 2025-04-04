import pandas as pd
from suapy.extractors.paae.Banco import Banco
from suapy.extractors.paae.PaaeEdital6Extractor import AlimentacaoConfig, PaaeEdital6Extractor
from suapy.services.Parser import Parser
from suapy.services.PlanilhaHandler import PlanilhaHandler


class PaaeUpdateE7Sheet(PaaeEdital6Extractor):
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

    def processar_aluno(self, aluno: dict) -> dict:
        """Processa um único aluno e retorna um dicionário com os dados atualizados."""
        matricula = aluno["Matrícula"]
        inscricao = aluno["Inscrição"]
        nome = aluno["Nome"]
        cpf = aluno.get("CPF")
        periodo = aluno.get("Período")

        banco = aluno.get("Banco", "")
        agencia = aluno.get("Agência", "")
        conta = aluno.get("No da Conta", "")
        operacao = aluno.get("Op.", "")
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
            "Alimentacao": self.is_true(aluno.get("Alimentacao", "FALSO")),
            "Moradia": self.is_true(aluno.get("Moradia", "FALSO")),
            "Transporte": self.is_true(aluno.get("Transporte", "FALSO")),
            "Impressao": self.is_true(aluno.get("Impressao", "FALSO")),
            "Estudo": self.is_true(aluno.get("Estudo", "FALSO")),
        }

        return dados_aluno

    def montar_resumo(
        self,
        lista_alimentacao: list[dict],
        lista_moradia: list[dict],
        lista_transporte: list[dict],
        lista_transporte_municipal: list[dict],
        lista_estudo: list[dict]
    ) -> pd.DataFrame:
        """Gera o DataFrame da aba de resumo com os valores de auxílio."""

        valores_auxilio = {
            "Alimentacao": 100,
            "Moradia": 250,
            "Transporte": 250,
            "Transporte Municipal": 200,
            "Estudo": 500,
        }

        resumo = [
            {
                "Tipo": "Alimentacao",
                "Qtd. Alunos": len(lista_alimentacao),
                "Valor individual": valores_auxilio["Alimentacao"],
                "Valor total": len(lista_alimentacao) * valores_auxilio["Alimentacao"],
            },
            {
                "Tipo": "Moradia",
                "Qtd. Alunos": len(lista_moradia),
                "Valor individual": valores_auxilio["Moradia"],
                "Valor total": len(lista_moradia) * valores_auxilio["Moradia"],
            },
            {
                "Tipo": "Transporte",
                "Qtd. Alunos": len(lista_transporte),
                "Valor individual": valores_auxilio["Transporte"],
                "Valor total": len(lista_transporte) * valores_auxilio["Transporte"],
            },
            {
                "Tipo": "Impressão***",
                "Qtd. Alunos": len(lista_transporte_municipal),
                "Valor individual": valores_auxilio["Transporte Municipal"],
                "Valor total": len(lista_transporte_municipal) * valores_auxilio["Transporte Municipal"],
            },
            {
                "Tipo": "Estudo",
                "Qtd. Alunos": len(lista_estudo),
                "Valor individual": valores_auxilio["Estudo"],
                "Valor total": len(lista_estudo) * valores_auxilio["Estudo"],
            }
        ]

        total_geral = sum(r["Valor total"] for r in resumo)
        resumo.append({
            "Tipo": "",
            "Qtd. Alunos": "",
            "Valor individual": "TOTAL",
            "Valor total": total_geral,
        })

        df = pd.DataFrame(resumo)
        df["Valor total"] = df["Valor total"].apply(
            lambda x: f"R$ {x:,.2f}".replace(
                ",", "X").replace(".", ",").replace("X", ".")
            if isinstance(x, (int, float)) else x
        )

        return df

    def montar_listas_especificas(self, lista_geral: list[dict]):

        lista_alimentacao = [aluno for aluno in lista_geral if self.is_true(
            aluno.get("Alimentacao", "FALSO"))]
        lista_moradia = [aluno for aluno in lista_geral if self.is_true(
            aluno.get("Moradia", "FALSO"))]
        lista_transporte = [aluno for aluno in lista_geral if self.is_true(
            aluno.get("Transporte", "FALSO"))]
        lista_impressao = [aluno for aluno in lista_geral if self.is_true(
            aluno.get("Impressao", "FALSO"))]
        lista_estudo = [aluno for aluno in lista_geral if self.is_true(
            aluno.get("Estudo", "FALSO"))]

        return (
            lista_alimentacao,
            lista_moradia,
            lista_transporte,
            lista_impressao,
            lista_estudo
        )

    def is_true(self, valor):
        if isinstance(valor, (int, float)):
            return valor != 0
        if isinstance(valor, bool):
            return valor is True
        return str(valor).strip().upper() == "VERDADEIRO"

    def exec(self) -> None:
        print("🔍 Atualizando dados PAAE")

        handler = PlanilhaHandler(self.arquivo_inscritos)
        dados_planilha = handler.ler_planilha(header=0, sheet_name=1)

        print(f"📊 Total de inscritos: {len(dados_planilha)}")

        lista_geral = []
        lista_sem_conta = []

        for i, aluno in enumerate(dados_planilha, 1):
            try:
                print(f"📥 Atualizando dados: {i} de {len(dados_planilha)}")
                dados_aluno = self.processar_aluno(aluno)
                lista_geral.append(dados_aluno)

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

        (
            lista_alimentacao,
            lista_moradia,
            lista_transporte,
            lista_impressao,
            lista_estudo
        ) = self.montar_listas_especificas(lista_geral)

        dados_por_abas = {
            "Resumo": self.montar_resumo(
                lista_alimentacao,
                lista_moradia,
                lista_transporte,
                lista_impressao,
                lista_estudo
            ),
            "Alunos": pd.DataFrame(lista_geral),
            "Alimentacao": pd.DataFrame(lista_alimentacao),
            "Moradia": pd.DataFrame(lista_moradia),
            "Transporte": pd.DataFrame(lista_transporte),
            "Impressao": pd.DataFrame(lista_impressao),
            "Estudo": pd.DataFrame(lista_estudo),
        }

        handler.salvar_planilha_por_abas(dados_por_abas, "Planilha_Edital_07")
        handler.salvar_planilha(
            lista_sem_conta, "Planilha_Edital_07_alunos_sem_conta")

    @staticmethod
    def main() -> None:
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/RelatóriosPAAE/Planilha_Edital_07_pagamento_de_Abril_de_2025.xlsx"

        paae_bot = PaaeUpdateE7Sheet(
            headless=True,
            arquivo_inscritos=inscritos_path,
        )
        paae_bot.exec()
