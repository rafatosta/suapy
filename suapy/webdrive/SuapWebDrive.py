from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from suapy.services.CredentialsManager import CredentialsManager


class SuapWebDrive:

    def __init__(self, headless=True, url="https://suap.ifba.edu.br/"):
        self.driver = self.setup_driver(headless)
        self.url = url

    def setup_driver(self, headless):
        """Configura e retorna o driver do Chrome com ou sem headless."""
        options = webdriver.ChromeOptions()
        if headless:
            # Ativa o modo headless apenas se necessário
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def login(self):
        """Realiza login no SUAP e aguarda o carregamento completo."""
        try:
            manager = CredentialsManager()
            username, password = manager.get_credentials()

            if username and password:
                self.driver.get(self.url)

                # Preenche e envia o formulário de login
                self.driver.find_element(
                    By.ID, "id_username").send_keys(username)
                password_field = self.driver.find_element(By.ID, "id_password")
                password_field.send_keys(password)
                password_field.submit()

                # 🔹 Aguarda um elemento que indica que o login foi concluído
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(
                        (By.ID, "user-tools"))  # pode mudar
                )

                # 🔹 Aguarda o carregamento total do SUAP antes de permitir outras navegações
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.execute_script(
                        "return document.readyState") == "complete"
                )

                print("✅ Login realizado e SUAP pronto para navegação!")
            else:
                print("⚠️ Nenhuma credencial disponível.")

        except Exception as e:
            print(f"❌ Erro ao tentar logar: {e}")
            self.close()

    def exec(self):
        """Lógica de execução do bot"""
        pass

    def load_page(self, url, timeout=10):
        """
        Carrega uma página no Selenium e aguarda até que a URL mude e o DOM esteja pronto.

        :param driver: Instância do WebDriver
        :param url: URL a ser carregada
        :param timeout: Tempo máximo de espera (padrão: 10s)
        """
        self.driver.get(url)
        self.driver.refresh()  # Garante o carregamento correto

        # Aguarda a URL ser atualizada
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.current_url == url)

        # Aguarda o DOM estar completamente carregado
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete"
        )

        # print(f"Página carregada: {url}")  # Debug

    def find_element(self, by, value, timeout=10):
        """
        Encontra um elemento na página com espera explícita.

        :param driver: Instância do WebDriver
        :param by: Tipo de busca (ex: By.XPATH, By.ID, By.CLASS_NAME)
        :param value: Valor do seletor
        :param timeout: Tempo máximo de espera (padrão: 10s)
        :return: Elemento encontrado
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def close(self):
        """Fecha o navegador."""
        self.driver.quit()

    @staticmethod
    def main():
        """Algoritmo para execução do extractor"""
        pass
