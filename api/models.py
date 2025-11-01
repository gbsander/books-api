from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    """Modelo que representa um livro"""
    id: int  # ID único do livro
    title: str  # Título
    price: float  # Preço
    rating: int  # Rating de 1 a 5
    availability: str  # "In stock" ou "Out of stock"
    category: str = "Unknown"  # Categoria do livro (default: Unknown)
    image_url: str  # URL da imagem

    class Config:
        # Exemplo de como o JSON vai aparecer na documentação
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "A Light in the Attic",
                "price": 51.77,
                "rating": 3,
                "availability": "In stock",
                "image_url": "https://books.toscrape.com/media/cache/..."
            }
        }


class HealthResponse(BaseModel):
    """Resposta do endpoint de health check"""
    status: str
    total_books: int
