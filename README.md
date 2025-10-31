# Books API - Tech Challenge

API RESTful para consultar dados de livros extraídos do site [books.toscrape.com](https://books.toscrape.com/).

## 📋 Descrição do Projeto

Este projeto implementa um **pipeline completo de dados**:
1. **Web Scraping**: Extração automatizada de dados de livros
2. **Armazenamento**: Dados salvos em formato CSV
3. **API REST**: Endpoints para consulta e busca de livros
4. **Documentação**: Swagger/OpenAPI automático

## 🏗️ Arquitetura

```
tc1_/
├── scripts/           # Web scraping
│   └── scraper.py    # Script de extração de dados
├── api/              # API RESTful
│   ├── main.py       # Aplicação FastAPI
│   ├── models.py     # Modelos Pydantic
│   └── services.py   # Lógica de negócio
├── data/             # Armazenamento
│   └── books.csv     # Dados extraídos
└── requirements.txt  # Dependências
```

### Pipeline de Dados
```
[Site] → [Scraper] → [CSV] → [API] → [Cliente]
```

## 🚀 Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone <seu-repositorio>
cd tc1_
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o scraping
```bash
python scripts/scraper.py
```
Isso vai gerar o arquivo `data/books.csv` com todos os livros.

### 5. Rodar a API
```bash
uvicorn api.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### Documentação Interativa (Swagger)
Acesse: `http://localhost:8000/docs`

### Endpoints Disponíveis

#### 1. Health Check
```http
GET /api/v1/health
```

**Resposta:**
```json
{
  "status": "ok",
  "total_books": 1000
}
```

#### 2. Listar Todos os Livros
```http
GET /api/v1/books
```

**Resposta:**
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
  ...
]
```

#### 3. Buscar Livro por ID
```http
GET /api/v1/books/{id}
```

**Exemplo:**
```bash
curl http://localhost:8000/api/v1/books/1
```

**Resposta:**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": "In stock",
  "image_url": "https://books.toscrape.com/media/cache/..."
}
```

#### 4. Buscar Livros por Título
```http
GET /api/v1/books/search?title={termo}
```

**Exemplo:**
```bash
curl "http://localhost:8000/api/v1/books/search?title=light"
```

**Resposta:**
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    ...
  }
]
```

#### 5. Listar Categorias
```http
GET /api/v1/categories
```

**Exemplo:**
```bash
curl http://localhost:8000/api/v1/categories
```

**Resposta:**
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
  ...
]
```

## 🧪 Exemplos de Uso

### Usando cURL
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Listar todos
curl http://localhost:8000/api/v1/books

# Buscar por ID
curl http://localhost:8000/api/v1/books/5

# Buscar por título
curl "http://localhost:8000/api/v1/books/search?title=python"

# Listar categorias
curl http://localhost:8000/api/v1/categories
```

### Usando Python
```python
import requests

# Buscar todos os livros
response = requests.get("http://localhost:8000/api/v1/books")
books = response.json()
print(f"Total de livros: {len(books)}")

# Buscar livro específico
response = requests.get("http://localhost:8000/api/v1/books/1")
book = response.json()
print(f"Livro: {book['title']}")

# Buscar por título
response = requests.get("http://localhost:8000/api/v1/books/search",
                       params={"title": "light"})
results = response.json()
print(f"Encontrados: {len(results)} livros")
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: Servidor ASGI
- **BeautifulSoup4**: Web scraping
- **Pandas**: Manipulação de dados
- **Pydantic**: Validação de dados

## 📊 Estrutura dos Dados

Cada livro possui os seguintes campos:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | int | Identificador único |
| title | string | Título do livro |
| price | float | Preço em libras (£) |
| rating | int | Avaliação de 1 a 5 estrelas |
| availability | string | Status de disponibilidade |
| image_url | string | URL da imagem da capa |

## 🔄 Escalabilidade e Melhorias Futuras

### Melhorias Implementáveis:
1. **Banco de Dados**: Migrar de CSV para PostgreSQL/MongoDB
2. **Cache**: Implementar Redis para respostas rápidas
3. **Paginação**: Adicionar limit/offset nos endpoints
4. **Filtros**: Adicionar filtros por preço, rating, etc
5. **Autenticação**: JWT para endpoints protegidos
6. **Rate Limiting**: Limitar requisições por IP
7. **Testes**: Pytest para cobertura de testes
8. **CI/CD**: GitHub Actions para deploy automático

### Integração com Machine Learning:
```python
# Exemplo de uso para ML
import pandas as pd

# Carregar dados via API
response = requests.get("http://localhost:8000/api/v1/books")
df = pd.DataFrame(response.json())

# Preparar features para modelo
X = df[['price', 'rating']]
y = df['availability']

# Treinar modelo de classificação
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)
```

## 🚀 Deploy

### Deploy no Render (Gratuito)

1. Criar conta no [Render](https://render.com)
2. Criar novo Web Service
3. Conectar ao repositório GitHub
4. Configurar:
   - **Build Command**: `pip install -r requirements.txt && python scripts/scraper.py`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### Deploy no Fly.io

```bash
# Instalar Fly CLI
curl -L https://fly.io/install.sh | sh

# Fazer login
fly auth login

# Deploy
fly launch
fly deploy
```

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Tech Challenge.

## 👨‍💻 Autor

[Seu Nome]
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)

---

**Observação**: Este projeto realiza web scraping de forma ética e respeitosa, com delays entre requisições para não sobrecarregar o servidor alvo.
