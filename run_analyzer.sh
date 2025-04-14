#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando analyzer...${NC}"

# Verifica se o Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 não encontrado. Por favor, instale o Python3.${NC}"
    exit 1
fi

# Verifica se o diretório foi fornecido
if [ $# -eq 0 ]; then
    echo -e "${RED}Erro: Diretório não fornecido${NC}"
    echo "Uso: ./run_analyzer.sh <diretório_com_jsons>"
    exit 1
fi

# Verifica se o diretório existe
if [ ! -d "$1" ]; then
    echo -e "${RED}Erro: Diretório '$1' não encontrado${NC}"
    exit 1
fi

# Conta quantos arquivos JSON existem no diretório
json_count=$(find "$1" -name "*.json" | wc -l)

if [ "$json_count" -eq 0 ]; then
    echo -e "${RED}Erro: Nenhum arquivo JSON encontrado no diretório '$1'${NC}"
    exit 1
fi

echo -e "${GREEN}Encontrados $json_count arquivo(s) JSON para análise${NC}"

# Processa cada arquivo JSON no diretório
for json_file in "$1"/*.json; do
    echo -e "\n${GREEN}Processando arquivo: $(basename "$json_file")${NC}"
    python3 analyzer.py "$json_file"
done

echo -e "\n${GREEN}Processo concluído! Todos os arquivos foram analisados.${NC}" 