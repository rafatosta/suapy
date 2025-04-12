import pandas as pd
from suapy.extractors.paae.Banco import Banco
from suapy.extractors.paae.PaaeEdital6Extractor import AlimentacaoConfig, PaaeEdital6Extractor
from suapy.services.PlanilhaHandler import PlanilhaHandler


class PaaeUpdateE7BuildSheet(PaaeEdital6Extractor):
    def __init__(
        self,
        headless: bool = False,
        arquivo_inscritos: str = "",
    ):
        super().__init__(headless=headless)
        self.arquivo_inscritos = arquivo_inscritos

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
                "Qtd. Alunos": len(lista_alimentacao) - 1,
                "Valor individual": valores_auxilio["Alimentacao"],
                "Valor total": (len(lista_alimentacao) - 1) * valores_auxilio["Alimentacao"],
            },
            {
                "Tipo": "Moradia",
                "Qtd. Alunos": len(lista_moradia) - 1,
                "Valor individual": valores_auxilio["Moradia"],
                "Valor total": (len(lista_moradia) - 1) * valores_auxilio["Moradia"],
            },
            {
                "Tipo": "Transporte",
                "Qtd. Alunos": len(lista_transporte) - 1,
                "Valor individual": valores_auxilio["Transporte"],
                "Valor total": (len(lista_transporte) - 1) * valores_auxilio["Transporte"],
            },
            {
                "Tipo": "Transporte Municipal",
                "Qtd. Alunos": len(lista_transporte_municipal) - 1,
                "Valor individual": valores_auxilio["Transporte Municipal"],
                "Valor total": (len(lista_transporte_municipal) - 1) * valores_auxilio["Transporte Municipal"],
            },
            {
                "Tipo": "Estudo",
                "Qtd. Alunos": len(lista_estudo) - 1,
                "Valor individual": valores_auxilio["Estudo"],
                "Valor total": (len(lista_estudo) - 1) * valores_auxilio["Estudo"],
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

    def exec(self):
        handler = PlanilhaHandler(self.arquivo_inscritos)

        abas_auxilios = ["Alimentação", "Moradia", "Transporte", "Estudo"]
        dados_completos = {}

        for aba in abas_auxilios:
            dados = handler.ler_planilha(sheet_name=aba)
            df = pd.DataFrame(dados)
            df[aba] = True  # Marca que o aluno está inscrito nesse auxílio

            for _, row in df.iterrows():
                matricula = row["Matrícula"]

                if matricula not in dados_completos:
                    # Inicializa registro com todos os campos
                    dados_completos[matricula] = {
                        "Inscrição": row.get("Inscrição"),
                        "Matrícula": matricula,
                        "Nome": row.get("Nome"),
                        "Período": row.get("Período"),
                        "CPF": row.get("CPF"),
                        "Banco": row.get("Banco"),
                        "Agência": row.get("Agência"),
                        "Número da Conta": row.get("Número da Conta"),
                        "Tipo de conta": row.get("Tipo de conta"),
                        "Op.": row.get("Op."),
                        "Alimentação": False,
                        "Moradia": False,
                        "Transporte": False,
                        "Estudo": False,
                    }

                dados_completos[matricula][aba] = True

        # Converte para DataFrame final
        df_geral = pd.DataFrame(dados_completos.values())

        # Ordena colunas na ordem desejada
        colunas_finais = [
            "Inscrição", "Matrícula", "Nome", "Período", "CPF",
            "Banco", "Agência", "Número da Conta", "Tipo de conta", "Op.",
            "Alimentação", "Moradia", "Transporte", "Estudo"
        ]
        df_geral = df_geral[colunas_finais]

        # Remove campos em branco (string vazia ou NaN)
        df_geral.replace("", pd.NA, inplace=True)
        df_geral.dropna(how="all", subset=[
            "Inscrição", "Matrícula", "Nome", "CPF"
        ], inplace=True)  # Garante que não removerá só por falta de banco, por exemplo

        print(df_geral)

        # Salva em nova aba (você pode ajustar isso conforme o handler que estiver usando)
        nome_arquivo_saida = "aba_geral_auxilios.xlsx"
        df_geral.to_excel(nome_arquivo_saida, index=False)
        print(f"✅ Planilha geral salva como '{nome_arquivo_saida}'")

    @staticmethod
    def main() -> None:
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/RelatóriosPAAE/Planilha_de_pagamento_de_Abril_de_2025.xlsx"
        paae_bot = PaaeUpdateE7BuildSheet(
            headless=True,
            arquivo_inscritos=inscritos_path,
        )
        paae_bot.exec()
