from suapy.webdrive.SuapWebDrive import SuapWebDrive
from selenium.webdriver.common.by import By


class PAAEBase (SuapWebDrive):

    def SUAP_INSCRICAO(self, inscricao):
        """Retorna a URL da inscrição do aluno no SUAP."""
        return f"https://suap.ifba.edu.br/ae/visualizarinscricaoae/{inscricao}/"

    def SUAP_MATRICULA(self, matricula):
        """Retorna a URL do perfil do aluno no SUAP."""
        return f"https://suap.ifba.edu.br/edu/aluno/{matricula}/"

    def access_student_profile(self, profile_id):
        try:
            self.load_page(self.SUAP_INSCRICAO(profile_id))

            linha = self.find_element(
                By.XPATH,
                '//table[contains(@class,"info")]//tr[td[contains(normalize-space(.),"Conta Bancária Escolhida")]]'
            )

            banco = linha.find_element(
                By.XPATH, './/dt[contains(.,"Banco:")]/following-sibling::dd[1]'
            ).text.strip()

            agencia = linha.find_element(
                By.XPATH, './/dt[contains(.,"Agência:")]/following-sibling::dd[1]'
            ).text.strip()

            conta = linha.find_element(
                By.XPATH, './/dt[contains(.,"Conta:")]/following-sibling::dd[1]'
            ).text.strip()

            operacao = linha.find_element(
                By.XPATH, './/dt[contains(.,"Operação:")]/following-sibling::dd[1]'
            ).text.strip()

            return {
                "banco": banco,
                "agencia": agencia,
                "conta": conta,
                "operacao": operacao
            }

        except Exception as e:
            print(f"Erro ao acessar perfil do estudante ({profile_id}): {e}")
            return {
                "banco": "",
                "agencia": "",
                "conta": "",
                "operacao": ""
            }

    def access_student_register(self, register_id):
        """
        Acessa o registro acadêmico do estudante e retorna o CPF e período.
        """
        try:
            self.load_page(self.SUAP_MATRICULA(register_id))
            table = self.find_element(
                By.XPATH,
                '//table[contains(@class,"info")]'
            )

            cpf = table.find_element(
                By.XPATH,
                './/tr[td[normalize-space(.)="CPF"]]/td[2]'
            ).text.strip()

            periodo = table.find_element(
                By.XPATH,
                './/tr[td[contains(normalize-space(.),"Período Referência")]]/td[2]'
            ).text.strip()

            curso = table.find_element(
                By.XPATH,
                './/tr[td[normalize-space(.)="Curso"]]/td[2]'
            ).text.strip()

            return {
                "cpf": cpf,
                "periodo": periodo,
                "curso": curso
            }

        except Exception as e:
            print(f"Erro ao obter dados do aluno: {e}")
            return {
                "cpf": "",
                "periodo": "",
                "curso": ""
            }
