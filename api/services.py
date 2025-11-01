import csv
from typing import List, Optional
from api.models import Book

# Variável global para armazenar os livros em memória
books_data: List[dict] = []


def load_books_from_csv(filepath: str = 'data/books.csv'):
    """Carrega os livros do CSV para memória"""
    global books_data

    # Lê o CSV usando biblioteca csv nativa
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        books_data = list(reader)

    # Adiciona ID sequencial e converte tipos
    for i, book in enumerate(books_data, start=1):
        book['id'] = i
        book['price'] = float(book['price'])
        book['rating'] = int(book['rating'])
        # Garante que category existe (retrocompatibilidade com CSV antigo)
        if 'category' not in book or not book['category']:
            book['category'] = 'Unknown'

    print(f"✓ {len(books_data)} livros carregados do CSV")


def get_all_books() -> List[Book]:
    """Retorna todos os livros"""
    return [Book(**book) for book in books_data]


def get_book_by_id(book_id: int) -> Optional[Book]:
    """Busca um livro pelo ID"""
    for book in books_data:
        if book['id'] == book_id:
            return Book(**book)
    return None  # Não encontrou


def search_books(title: Optional[str] = None) -> List[Book]:
    """Busca livros por título (case-insensitive)"""
    if not title:
        return get_all_books()

    # Filtra livros cujo título contém o termo buscado
    results = []
    for book in books_data:
        if title.lower() in book['title'].lower():
            results.append(Book(**book))

    return results
