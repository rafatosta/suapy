from suapy.webdrive.SuapWebDrive import SuapWebDrive


class PaaeExtractor(SuapWebDrive):

    def __init__(self, headless=False):
        super().__init__(headless=headless)

    def exec(self):
        print("Gerenciador PAAE")

        self.login()

        input("Pressione qualquer tecla para finalizar...")
        self.close()
