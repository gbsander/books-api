# Documentação Completa dos Endpoints

## Base URL
- **Local**: `http://localhost:8000`
- **Produção**: `https://seu-app.onrender.com`

## Todos os Endpoints Implementados

### 1. GET /api/v1/health
**Descrição**: Verifica se a API está funcionando e quantos livros estão carregados

**Request**:
```bash
curl http://localhost:8000/api/v1/health
```

**Response (200 OK)**:
```json
{
  "status": "ok",
  "total_books": 1000
}
```

---

### 2. GET /api/v1/books
**Descrição**: Lista todos os livros disponíveis na base de dados

**Request**:
```bash
curl http://localhost:8000/api/v1/books
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "availability": "In stock",
    "image_url": "https://books.toscrape.com/media/cache/..."
  },
  {
    "id": 2,
    "title": "Tipping the Velvet",
    "price": 53.74,
    "rating": 1,
    "availability": "In stock",
    "image_url": "https://books.toscrape.com/media/cache/..."
  }
  // ... mais 998 livros
]
```

---

### 3. GET /api/v1/books/{id}
**Descrição**: Retorna detalhes completos de um livro específico pelo ID

**Parâmetros**:
- `id` (path, obrigatório): ID do livro (inteiro)

**Request**:
```bash
curl http://localhost:8000/api/v1/books/5
```

**Response (200 OK)**:
```json
{
  "id": 5,
  "title": "Sapiens: A Brief History of Humankind",
  "price": 54.23,
  "rating": 5,
  "availability": "In stock",
  "image_url": "https://books.toscrape.com/media/cache/..."
}
```

**Response (404 Not Found)**:
```json
{
  "detail": "Livro com ID 9999 não encontrado"
}
```

---

### 4. GET /api/v1/books/search
**Descrição**: Busca livros por título (case-insensitive, busca parcial)

**Query Parameters**:
- `title` (query, opcional): Termo de busca no título

**Requests**:
```bash
# Buscar "light" no título
curl "http://localhost:8000/api/v1/books/search?title=light"

# Sem parâmetro = retorna todos
curl http://localhost:8000/api/v1/books/search
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "availability": "In stock",
    "image_url": "https://books.toscrape.com/media/cache/..."
  }
]
```

**Response (200 OK) - Sem resultados**:
```json
[]
```

---

### 5. GET /api/v1/categories
**Descrição**: Lista todas as categorias de avaliação disponíveis com contagem de livros

**Request**:
```bash
curl http://localhost:8000/api/v1/categories
```

**Response (200 OK)**:
```json
[
  {
    "name": "1 Star",
    "count": 226
  },
  {
    "name": "2 Stars",
    "count": 196
  },
  {
    "name": "3 Stars",
    "count": 203
  },
  {
    "name": "4 Stars",
    "count": 179
  },
  {
    "name": "5 Stars",
    "count": 196
  }
]
```

---

## Códigos de Status HTTP

| Código | Significado | Quando ocorre |
|--------|-------------|---------------|
| 200 | OK | Requisição bem-sucedida |
| 404 | Not Found | Livro não encontrado |
| 422 | Unprocessable Entity | Parâmetros inválidos (ex: ID não é número) |
| 500 | Internal Server Error | Erro no servidor |

---

## Exemplos de Uso em Diferentes Linguagens

### JavaScript (Fetch API)
```javascript
// Buscar todos os livros
fetch('http://localhost:8000/api/v1/books')
  .then(response => response.json())
  .then(books => console.log(books));

// Buscar por ID
fetch('http://localhost:8000/api/v1/books/5')
  .then(response => response.json())
  .then(book => console.log(book.title));

// Buscar por título
fetch('http://localhost:8000/api/v1/books/search?title=python')
  .then(response => response.json())
  .then(results => console.log(results));
```

### Python (requests)
```python
import requests

BASE_URL = "http://localhost:8000"

# Buscar todos
response = requests.get(f"{BASE_URL}/api/v1/books")
books = response.json()
print(f"Total: {len(books)}")

# Buscar por ID
response = requests.get(f"{BASE_URL}/api/v1/books/5")
book = response.json()
print(f"Livro: {book['title']}")

# Buscar por título
response = requests.get(
    f"{BASE_URL}/api/v1/books/search",
    params={"title": "python"}
)
results = response.json()
print(f"Encontrados: {len(results)}")

# Listar categorias
response = requests.get(f"{BASE_URL}/api/v1/categories")
categories = response.json()
for cat in categories:
    print(f"{cat['name']}: {cat['count']} livros")
```

### cURL com Headers
```bash
# Com header Accept
curl -H "Accept: application/json" \
     http://localhost:8000/api/v1/books/1

# Salvando resposta em arquivo
curl http://localhost:8000/api/v1/books \
     -o books.json

# Com verbose (mostra headers)
curl -v http://localhost:8000/api/v1/health
```

---

## Documentação Interativa (Swagger)

Acesse `/docs` para documentação interativa onde você pode:
- Ver todos os endpoints
- Testar diretamente no navegador
- Ver schemas dos modelos
- Baixar OpenAPI spec

**URL**: `http://localhost:8000/docs`

---

## Limitações e Melhorias Futuras

### Atuais:
- ❌ Sem paginação (retorna todos os ~1000 livros)
- ❌ Sem autenticação
- ❌ Sem rate limiting
- ❌ Busca só por título (não por preço, rating, etc)

### Planejadas:
- ✅ Paginação: `?page=1&limit=50`
- ✅ Filtros múltiplos: `?min_price=10&max_price=50&rating=5`
- ✅ Ordenação: `?sort_by=price&order=desc`
- ✅ Autenticação JWT
- ✅ Rate limiting (ex: 100 req/min por IP)
