#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para limpar o terminal e mostrar mensagem de saída
cleanup() {
    echo -e "\n${GREEN}Keylogger finalizado com sucesso!${NC}"
    echo -e "${GREEN}Os dados foram salvos em keylog.json${NC}"
    exit 0
}

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não está instalado. Por favor, instale o Python 3 primeiro.${NC}"
    exit 1
fi

# Verifica se as dependências estão instaladas
echo "Verificando dependências..."
pip3 install -r requirements.txt

# Limpa o terminal
clear

# Mostra mensagem de início
echo -e "${GREEN}Iniciando o Keylogger...${NC}"
echo -e "${GREEN}Pressione F12 para finalizar${NC}"
echo "----------------------------------------"

# Executa o keylogger
python3 keylogger.py 