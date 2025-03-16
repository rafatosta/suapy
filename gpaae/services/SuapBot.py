import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


class SuapBot:

    relatorio_alunos_inscritos = "https://suap.ifba.edu.br/ae/relatorio_alunos_inscritos/"

    def __init__(self, headless=True):  # Flag para ativar/desativar o modo headless
        self.driver = self.setup_driver(headless)

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

    def perform_login(self, username, password):
        """Realiza login no SUAP."""
        try:
            self.driver.get(self.relatorio_alunos_inscritos)
            self.driver.find_element(By.NAME, "username").send_keys(username)
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)
            password_field.submit()
        except Exception as e:
            print(f"Erro ao tentar logar: {e}")

    def get_report_params(self):
        try:
            if self.relatorio_alunos_inscritos in self.driver.current_url:
                print("Página correta dos relatórios")

                # Filtrar por ano
                select_element = self.driver.find_element(By.ID, "id_ano")  # Pode ser por NAME, XPATH, etc.
                select = Select(select_element)
                options = select.options  # Retorna uma lista de WebElements
                option_texts = [option.text for option in options]  # Pega apenas os textos
                print(option_texts)

                # Filtrar por edital
                select_element = self.driver.find_element(By.ID, "id_edital_ae")  # Pode ser por NAME, XPATH, etc.
                select = Select(select_element)
                options = select.options  # Retorna uma lista de WebElements
                option_texts = [option.text for option in options]  # Pega apenas os textos
                print(option_texts)

                # Filtrar por campus
                select_element = self.driver.find_element(By.ID, "id_campus")  # Pode ser por NAME, XPATH, etc.
                select = Select(select_element)
                options = select.options  # Retorna uma lista de WebElements
                option_texts = [option.text for option in options]  # Pega apenas os textos
                print(option_texts)

                # Filtrar por Situação da Documentação:
                select_element = self.driver.find_element(By.ID, "id_situacao_documentacao")  # Pode ser por NAME, XPATH, etc.
                select = Select(select_element)
                options = select.options  # Retorna uma lista de WebElements
                option_texts = [option.text for option in options]  # Pega apenas os textos
                print(option_texts)

                # Filtrar por Situação Resultado
                select_element = self.driver.find_element(By.ID, "id_situacao_resultado")  # Pode ser por NAME, XPATH, etc.
                select = Select(select_element)
                options = select.options  # Retorna uma lista de WebElements
                option_texts = [option.text for option in options]  # Pega apenas os textos
                print(option_texts)


        # Otimizar; fazer a seleção dos campus; e fazer o submit

        except Exception as e:
            print(f"Erro ao tentar acessar o relatório: {e}")

    def close(self):
        """Fecha o navegador."""
        self.driver.quit()
