

from suapy.extractors.PaaeExtractor import AlimentacaoConfig, PaaeExtractor


def main():

    # Caminho do arquivo com os alunos inscritos
    alunos_inscritos = "/home/tosta/Documentos/GitHub/gerenciador-paae/Lista_alunos.xls"
    alunos_removidos = "/home/tosta/Documentos/GitHub/gerenciador-paae/Lista_alunos_removidos.xls"

    config = AlimentacaoConfig(
        data_inicio="01/03/2025",
        data_fim="01/04/2025",
    )

    paae_bot = PaaeExtractor(
        headless=True,
        arquivo_inscritos=alunos_inscritos,
        arquivos_removidos=alunos_removidos,
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