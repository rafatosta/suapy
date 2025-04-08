import pandas as pd
from suapy.extractors.paae.Banco import Banco
from suapy.extractors.paae.PaaeEdital6Extractor import AlimentacaoConfig, PaaeEdital6Extractor
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

    def is_true(self, valor) -> bool:
        if isinstance(valor, (int, float)):
            return valor != 0
        if isinstance(valor, bool):
            return valor
        return str(valor).strip().upper() == "VERDADEIRO"

    def processar_aluno(self, aluno: dict) -> dict:
        """Processa um único aluno e retorna um dicionário com os dados atualizados."""
        tipo_conta = Banco.tipo_de_conta(
            aluno.get("Banco", ""), aluno.get("Op.", ""))

        return {
            "Inscrição": aluno["Inscrição"],
            "Matrícula": aluno["Matrícula"],
            "Nome": aluno["Nome"],
            "Período": aluno.get("Período"),
            "CPF": aluno.get("CPF"),
            "Banco": aluno.get("Banco", ""),
            "Agência": aluno.get("Agência", ""),
            "Número da Conta": aluno.get("Número da Conta", ""),
            "Tipo de Conta": tipo_conta,
            "Op.": aluno.get("Op.", ""),
            "Alimentação": self.is_true(aluno.get("Alimentação", "FALSO")),
            "Moradia": self.is_true(aluno.get("Moradia", "FALSO")),
            "Transporte": self.is_true(aluno.get("Transporte", "FALSO")),
            "Transporte Municipal": self.is_true(aluno.get("Transporte Municipal", "FALSO")),
            "Estudo": self.is_true(aluno.get("Estudo", "FALSO")),
        }

    def montar_listas_especificas(self, lista_geral: list[dict]):
        """Separa a lista geral em listas por tipo de auxílio, removendo os campos dos auxílios e incluindo o campo Valor e Total."""
        chaves = ["Alimentação", "Moradia",
                  "Transporte", "Transporte Municipal", "Estudo"]
        valores = {
            "Alimentação": 100,
            "Moradia": 250,
            "Transporte": 250,
            "Transporte Municipal": 200, 
            "Estudo": 500,
        }

        listas_especificas = []

        for chave in chaves:
            lista = []
            for aluno in lista_geral:
                if self.is_true(aluno.get(chave, "FALSO")):
                    aluno_limpo = {k: v for k,
                                   v in aluno.items() if k not in chaves}
                    aluno_limpo["Valor"] = valores[chave]
                    lista.append(aluno_limpo)

            # Adiciona linha de total ao final da lista
            total = sum(aluno["Valor"] for aluno in lista)
            lista.append({
                "Op.": "TOTAL",
                "Valor": f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            })

            listas_especificas.append(lista)

        return tuple(listas_especificas)

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
            "Alimentação": 100,
            "Moradia": 250,
            "Transporte": 250,
            "Transporte Municipal": 200,
            "Estudo": 500,
        }

        resumo = [
            {
                "Tipo": "Alimentação",
                "Qtd. Alunos": len(lista_alimentacao) - 1,
                "Valor individual": valores_auxilio["Alimentação"],
                "Valor total": (len(lista_alimentacao) - 1) * valores_auxilio["Alimentação"],
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
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            if isinstance(x, (int, float)) else x
        )

        return df


    def exec(self) -> None:
        print("🔍 Atualizando dados PAAE")

        handler = PlanilhaHandler(self.arquivo_inscritos)
        dados_planilha = handler.ler_planilha(header=0)
        print(f"📊 Total de inscritos: {len(dados_planilha)}")

        lista_geral = []
        lista_sem_conta = []

        for i, aluno in enumerate(dados_planilha, 1):
            try:
                print(f"📥 Atualizando dados: {i} de {len(dados_planilha)}")
                dados_aluno = self.processar_aluno(aluno)
                lista_geral.append(dados_aluno)

                if not all([
                    dados_aluno["Banco"],
                    dados_aluno["Agência"],
                    dados_aluno["Número da Conta"],
                    dados_aluno["Op."]
                ]):
                    lista_sem_conta.append(dados_aluno)

            except Exception as e:
                print(f"❌ [Erro] Linha {i}: Campos inválidos!")
                print(e)

        listas = self.montar_listas_especificas(lista_geral)
        dados_por_abas = {
            "Resumo": self.montar_resumo(*listas),
            "Alunos": pd.DataFrame(lista_geral),
            "Alimentação": pd.DataFrame(listas[0]),
            "Moradia": pd.DataFrame(listas[1]),
            "Transporte": pd.DataFrame(listas[2]),
            "Transporte Municipal": pd.DataFrame(listas[3]),
            "Estudo": pd.DataFrame(listas[4]),
        }

        handler.salvar_planilha_por_abas(dados_por_abas, "Planilha_Edital_07")
        handler.salvar_planilha(
            lista_sem_conta, "Planilha_Edital_07_alunos_sem_conta")

    @staticmethod
    def main() -> None:
        #inscritos_path = "/home/tosta/Documentos/GitHub/suapy/RelatóriosPAAE/Planilha_Edital_07_pagamento_de_Abril_de_2025.xlsx"
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/aba_geral_auxilios.xlsx"
        paae_bot = PaaeUpdateE7Sheet(
            headless=True,
            arquivo_inscritos=inscritos_path,
        )
        paae_bot.exec()
