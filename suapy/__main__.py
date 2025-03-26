

from suapy.extractors.paae.PaaeExtractor import AlimentacaoConfig, PaaeExtractor


def main():

    # Caminho do arquivo com os alunos inscritos
    alunos_inscritos = "/home/tosta/Documentos/PAAE-Editais/edital_6.xls"
    alunos_removidos = "/home/tosta/Documentos/PAAE-Editais/edital_6_remover.xls"

    config = AlimentacaoConfig(
        data_inicio="01/04/2025",
        data_fim="30/04/2025",
    )

    paae_bot = PaaeExtractor(
        headless=False,
        arquivo_inscritos=alunos_inscritos,
        arquivos_removidos=alunos_removidos,
        alimentacao_config=config
    )
    paae_bot.exec()


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
