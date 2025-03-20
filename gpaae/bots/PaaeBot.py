from gpaae.services.CredentialsManager import CredentialsManager
from gpaae.webdrive.SuapWebDrive import SuapWebDrive


class PaaeBot(SuapWebDrive):

    relatorio_alunos_inscritos = "https://suap.ifba.edu.br/ae/relatorio_alunos_inscritos/"

    def __init__(self, headless=False):
        super().__init__(headless=headless, url=self.relatorio_alunos_inscritos)

    def exec(self):
        print("Gerenciador PAAE")

        self.login()

        input("Pressione qualquer tecla para finalizar...")
        self.close()
