#!/bin/bash

# Script executado durante o build no Render

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Executando web scraping..."
python scripts/scraper.py

echo "Build concluído!"
