from gpaae.services.CredentialsManager import CredentialsManager
from gpaae.services.SuapBot import SuapBot


def main():
    print("Gerenciador PAAE")

    manager = CredentialsManager()
    username, password = manager.get_credentials()

    if username and password:

        print("Realizando login SUAP.")
        bot = SuapBot(headless=False)  # Executa com interface gráfica
        bot.perform_login(username, password)

        print("Acessando página de relatórios")
        bot.get_report_params()

    else:
        print("Nenhuma credencial disponível.")

    input("Pressione qualquer tecla para finalizar...")
    bot.close()


if __name__ == "__main__":
    main()
