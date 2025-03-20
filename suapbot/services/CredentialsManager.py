import os
from dotenv import load_dotenv, set_key

class CredentialsManager:
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        load_dotenv(self.env_file, override=True)

    def save_credentials(self, username: str, password: str):
        set_key(self.env_file, "LOGIN", username)
        set_key(self.env_file, "PASSWORD", password)
        print("Credenciais salvas com sucesso!")

        # Recarrega as variáveis para garantir que a atualização seja refletida
        load_dotenv(self.env_file, override=True)

    def get_credentials(self):
        username = os.getenv("LOGIN")
        password = os.getenv("PASSWORD")
        if username and password:
            return username, password
        print("Nenhuma credencial encontrada.")
        return None, None

    def show_credentials(self):
        username, password = self.get_credentials()
        if username and password:
            print(f"Usuário: {username}\nSenha: {password}")
        else:
            print("Nenhuma credencial disponível.")