import pandas as pd
from typing import List, Optional
from api.models import Book

# Variável global para armazenar os livros em memória
books_data: List[dict] = []


def load_books_from_csv(filepath: str = 'data/books.csv'):
    """Carrega os livros do CSV para memória"""
    global books_data

    # Lê o CSV usando pandas
    df = pd.read_csv(filepath)

    # Converte para lista de dicionários e adiciona ID
    books_data = df.to_dict('records')
    for i, book in enumerate(books_data, start=1):
        book['id'] = i  # Adiciona ID sequencial

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
