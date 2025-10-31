#!/bin/bash

# Script executado durante o build no Render

set -e  # Para em caso de erro

echo "Atualizando pip..."
pip install --upgrade pip

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Executando web scraping..."
python scripts/scraper.py

echo "Build concluído!"
