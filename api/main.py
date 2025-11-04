from fastapi import FastAPI, HTTPException
from typing import List, Optional
from api.models import Book, HealthResponse
from api.services import load_books_from_csv, get_all_books, get_book_by_id, search_books

# Cria a aplicação FastAPI
app = FastAPI(
    title="Books API",
    description="API para consultar livros do site books.toscrape.com",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    """Executado quando a API inicia"""
    print("=" * 50)
    print("🚀 Iniciando Books API...")
    print("=" * 50)
    try:
        load_books_from_csv()
        print("✅ API pronta!")
        print("📊 Acesse /docs para documentação Swagger")
    except Exception as e:
        print(f"❌ ERRO no startup: {e}")
        import traceback
        traceback.print_exc()
        raise


# ========== ENDPOINTS ==========

@app.get("/")
def root():
    """Endpoint raiz - usado para health check do Render"""
    return {"message": "Books API está rodando!", "status": "ok"}


@app.get("/api/v1/health", response_model=HealthResponse)
def health_check():
    """Verifica se a API está funcionando"""
    books = get_all_books()
    return {
        "status": "ok",
        "total_books": len(books)
    }


@app.get("/api/v1/books", response_model=List[Book])
def list_books():
    """Lista todos os livros disponíveis"""
    return get_all_books()


@app.get("/api/v1/books/search", response_model=List[Book])
def search(title: Optional[str] = None):
    """Busca livros por título

    Exemplo: /api/v1/books/search?title=light
    """
    results = search_books(title)
    return results


@app.get("/api/v1/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """Retorna detalhes de um livro específico pelo ID"""
    book = get_book_by_id(book_id)

    # Se não encontrou, retorna erro 404
    if not book:
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado")

    return book


@app.get("/api/v1/categories")
def list_categories():
    """Lista todas as categorias de livros disponíveis"""
    books = get_all_books()

    # Agrupa por categoria e conta
    categories = {}
    for book in books:
        category = book.category

        if category not in categories:
            categories[category] = 0
        categories[category] += 1

    # Formata resposta ordenada por nome
    result = [
        {"name": name, "count": count}
        for name, count in sorted(categories.items())
    ]

    return result
