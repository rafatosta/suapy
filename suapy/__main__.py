from suapy.extractors.paae.PaaeUpdateE6Sheet import PaaeUpdateE6Sheet


def main():
    #PaaeEdital6Extractor.main()

    PaaeUpdateE6Sheet.main()


if __name__ == "__main__":
    main()

"""

PaaeExtractor -> Coleta dados para o PAAE
    Entrada: Planilha com estudantes

ConselhoBot -> Coleta dados para o conselho
    Entrada: Planilha com código das turmas

"""


"""
No perfil do aluno, o Período Referência não indica a série atual, mas a quantidade de anos que o aluno está na instituição. 
Solução: Pegar o código do último ano letivo (20241.4.0021.1N)?
"""
