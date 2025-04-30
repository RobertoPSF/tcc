#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'


if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 não encontrado. Por favor, instale o Python3.${NC}"
    exit 1
fi

echo "Verificando dependências..."
pip3 install -r analyzer_requirements.txt
clear

if [ $# -eq 0 ]; then
    echo -e "${RED}Erro: Diretório não fornecido${NC}"
    echo "Uso: ./run_analyzer.sh <diretório_com_jsons>"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo -e "${RED}Erro: Diretório '$1' não encontrado${NC}"
    exit 1
fi

json_count=$(find "$1" -name "*.json" | wc -l)

if [ "$json_count" -eq 0 ]; then
    echo -e "${RED}Erro: Nenhum arquivo JSON encontrado no diretório '$1'${NC}"
    exit 1
fi


for json_file in "$1"/*.json; do
    echo -e "\n${GREEN}Processando arquivo: $(basename "$json_file")${NC}"
    python3 analyzer.py "$json_file"
done

echo -e "\n${GREEN}Processo concluído! Todos os arquivos foram analisados.${NC}" 