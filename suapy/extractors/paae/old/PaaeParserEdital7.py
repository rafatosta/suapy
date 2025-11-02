import pandas as pd
from suapy.extractors.paae.old.PaaeEdital6Extractor import PaaeEdital6Extractor
from suapy.services.PlanilhaHandler import PlanilhaHandler


class PaaeParserEdital7(PaaeEdital6Extractor):
    def __init__(
        self,
        headless: bool = False,
        arquivo_inscritos: str = "",
    ):
        super().__init__(headless=headless)
        self.arquivo_inscritos = arquivo_inscritos

    def exec(self):
        handler = PlanilhaHandler(self.arquivo_inscritos)

        abas_auxilios = ["Alimentação", "Moradia", "Transporte", "Estudo"]
        dados_por_aba = {}

        # Lê os dados de cada aba e organiza por matrícula
        for aba in abas_auxilios:
            dados: list = handler.ler_planilha(sheet_name=aba)
            dados_limpos = [
                {k: v for k, v in item.items() if v not in (None, "", [], {})}
                for item in dados
            ]
            dados_filtrados = [
                item for item in dados_limpos
                if "Matrícula" in item and "Nome" in item and item["Matrícula"] and item["Nome"]
            ]
            dados_por_aba[aba] = dados_filtrados

        # Construir dicionário único por matrícula
        dados_completos_dict = {}

        for aba, dados in dados_por_aba.items():
            for item in dados:
                matricula = item["Matrícula"]
                if matricula not in dados_completos_dict:
                    # Inicializa com todos os dados e marcação dos auxílios como False
                    dados_completos_dict[matricula] = {
                        "Inscrição": item.get("Inscrição", ""),
                        "Matrícula": matricula,
                        "Nome": item.get("Nome", ""),
                        "Período": item.get("Período", ""),
                        "CPF": item.get("CPF", ""),
                        "Banco": item.get("Banco", ""),
                        "Agência": item.get("Agência", ""),
                        "Número da Conta": item.get("Número da Conta", ""),
                        "Tipo de conta": item.get("Tipo de conta", ""),
                        "Op.": item.get("Op.", ""),
                        "Alimentação": False,
                        "Moradia": False,
                        "Transporte": False,
                        "Transporte Municipal": False,
                        "Estudo": False,
                    }
                # Marca o auxílio como True
                dados_completos_dict[matricula][aba] = True
                print(item)

        dados_finais = list(dados_completos_dict.values())

        print("Total de registros combinados:", len(dados_finais))
        handler.salvar_planilha(dados_finais, "Planilha_Edital_07_AtualCompilado")


            
    @staticmethod
    def main() -> None:
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/Editais/PAAE-Relatórios-Atuais/Planilha_de_pagamento_de_Abril_de_2025.xlsx"
        paae_bot = PaaeParserEdital7(
            headless=True,
            arquivo_inscritos=inscritos_path,
        )
        paae_bot.exec()
