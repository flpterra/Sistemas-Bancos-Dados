#!/usr/bin/env bash
# Sistemas de Banco de Dados I
# Prepara o Codespace para usar notebooks Jupyter com o PostgreSQL.
# Executar no terminal, dentro da pasta da atividade:
#     bash preparar-jupyter.sh
set -e

echo "[1/5] Conferindo o servidor PostgreSQL..."
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^postgres_container$'; then
    echo "      postgres_container em execucao."
else
    echo "      ATENCAO: postgres_container nao esta em execucao."
    echo "      Na raiz do repositorio, executar: docker compose up -d"
fi

echo "[2/5] Instalando o Python (pode levar alguns instantes)..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-venv python3-pip > /dev/null

echo "[3/5] Criando o ambiente da disciplina em ~/.venv-sbd..."
python3 -m venv "$HOME/.venv-sbd"
"$HOME/.venv-sbd/bin/pip" install -q --upgrade pip
"$HOME/.venv-sbd/bin/pip" install -q jupysql psycopg2-binary pandas matplotlib ipykernel nbconvert

echo "[4/5] Registrando o kernel SBD (Python 3)..."
"$HOME/.venv-sbd/bin/python" -m ipykernel install --user --name sbd --display-name "SBD (Python 3)" > /dev/null

echo "[5/5] Instalando as extensoes Jupyter e Python no VS Code..."
if command -v code > /dev/null 2>&1; then
    code --install-extension ms-python.python --force > /dev/null 2>&1 || true
    code --install-extension ms-toolsai.jupyter --force > /dev/null 2>&1 || true
    echo "      Extensoes instaladas."
else
    echo "      Instalar pela aba Extensoes: Python e Jupyter, ambas da Microsoft."
fi

echo
echo "Pronto. Ao abrir um notebook, escolher o kernel 'SBD (Python 3)'"
echo "em Select Kernel, Jupyter Kernel."
