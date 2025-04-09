import pandas as pd
from suapy.extractors.paae.PaaeEdital6Extractor import PaaeEdital6Extractor
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
        dados_completos = []

        for aba in abas_auxilios:
            dados:list = handler.ler_planilha(sheet_name=aba)
            dados_completos.append({"TIPO":aba})
            dados_completos.extend(dados)  

        
        # Remover campos vazios de cada dicionário
        dados_limpos = [
            {k: v for k, v in item.items() if v not in (None, "", [], {})}
            for item in dados_completos
        ]

        print("Total de dados combinados:", len(dados_limpos))
        #print(dados_completos)
        handler.salvar_planilha(
            dados_limpos, "Planilha_Edital_07_Completos")

            
    @staticmethod
    def main() -> None:
        inscritos_path = "/home/tosta/Documentos/GitHub/suapy/Editais/PAAE-Relatórios-Atuais/Planilha_de_pagamento_de_Abril_de_2025.xlsx"
        paae_bot = PaaeParserEdital7(
            headless=True,
            arquivo_inscritos=inscritos_path,
        )
        paae_bot.exec()
