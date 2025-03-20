import os
import subprocess
import sys

# Nome do ambiente virtual
VENV_DIR = "venv"

# Verifica se o ambiente virtual já existe
if not os.path.exists(VENV_DIR):
    print("Criando ambiente virtual...")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR])

# Ativar o ambiente virtual
activate_script = os.path.join(VENV_DIR, "bin", "activate")
print(f"Ativando ambiente virtual: {activate_script}")

# Instalar ou atualizar o pip dentro do ambiente virtual
subprocess.run([os.path.join(VENV_DIR, "bin", "pip"), "install", "--upgrade", "pip"])

# Instalar dependências a partir do arquivo requirements.txt
requirements_file = 'requirements.txt'
if os.path.exists(requirements_file):
    print(f"Instalando dependências de {requirements_file}...")
    subprocess.run([os.path.join(VENV_DIR, "bin", "pip"), "install", "-r", requirements_file])
else:
    print(f"Nenhum arquivo {requirements_file} encontrado. Instalando 'suapbot'...")
    subprocess.run([os.path.join(VENV_DIR, "bin", "pip"), "install", "suapbot"])

# Executar o comando dentro do ambiente virtual
print("Executando o comando python -m suapbot...")
subprocess.run([os.path.join(VENV_DIR, "bin", "python"), "-m", "suapbot"])
