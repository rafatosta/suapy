

from suapy.extractors.PaaeExtractor import PaaeExtractor


def main():

    paae_bot = PaaeExtractor()
    paae_bot.exec()


if __name__ == "__main__":
    main()

"""

PaaeExtractor -> Coleta dados para o PAAE
    Entrada: Planilha com estudantes

ConselhoBot -> Coleta dados para o conselho
    Entrada: Planilha com código das turmas

"""
