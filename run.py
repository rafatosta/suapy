import os
import subprocess
import sys
import platform

# Nome do ambiente virtual
VENV_DIR = "venv"

# Detecta o sistema operacional
IS_WINDOWS = platform.system() == "Windows"

print(f"Sistema Operacional: {platform.system()}")

# Define os caminhos corretos de acordo com o sistema
if IS_WINDOWS:
    PYTHON_BIN = os.path.join(VENV_DIR, "Scripts", "python.exe")
    PIP_BIN = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    ACTIVATE_SCRIPT = os.path.join(VENV_DIR, "Scripts", "activate.bat")
else:
    PYTHON_BIN = os.path.join(VENV_DIR, "bin", "python")
    PIP_BIN = os.path.join(VENV_DIR, "bin", "pip")
    ACTIVATE_SCRIPT = os.path.join(VENV_DIR, "bin", "activate")

# Criação do ambiente virtual, se necessário
if not os.path.exists(VENV_DIR):
    print("Criando ambiente virtual...")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)

print(f"Ativando ambiente virtual: {ACTIVATE_SCRIPT}")

# Atualiza o pip dentro do ambiente
subprocess.run([PYTHON_BIN, "-m", "pip", "install",
               "--upgrade", "pip"], check=True)

# Instala dependências
requirements_file = "requirements.txt"
if os.path.exists(requirements_file):
    print(f"Instalando dependências de {requirements_file}...")
    subprocess.run([PIP_BIN, "install", "-r", requirements_file], check=True)
else:
    print(
        f"Nenhum arquivo {requirements_file} encontrado. Instalando 'suapy'...")
    subprocess.run([PIP_BIN, "install", "suapy"], check=True)

# Executa o comando principal
print("Executando o comando: python -m suapy ...")
subprocess.run([PYTHON_BIN, "-m", "suapy"], check=True)
