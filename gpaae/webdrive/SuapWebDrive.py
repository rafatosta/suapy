from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from gpaae.services.CredentialsManager import CredentialsManager


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
        """Realiza login no SUAP."""
        try:
            manager = CredentialsManager()
            username, password = manager.get_credentials()
            if username and password:
                self.driver.get(self.url)
                self.driver.find_element(By.NAME, "username").send_keys(username)
                password_field = self.driver.find_element(By.NAME, "password")
                password_field.send_keys(password)
                password_field.submit()
        except Exception as e:
            print(f"Erro ao tentar logar: {e}")
            self.close()
    
    def exec(self):
        """Lógica de execução do bot"""
        pass

    def close(self):
        """Fecha o navegador."""
        self.driver.quit()
