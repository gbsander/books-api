#!/bin/bash

# Script executado durante o build no Render

set -e  # Para em caso de erro

echo "Atualizando pip..."
pip install --upgrade pip

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Verificando CSV..."
if [ ! -f data/books.csv ]; then
    echo "ERRO: CSV não encontrado! Execute o scraper localmente."
    exit 1
fi

echo "CSV encontrado com $(wc -l < data/books.csv) linhas"
echo "Build concluído!"
