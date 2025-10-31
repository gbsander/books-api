# Plano Arquitetural - Books API

## 1. Visão Geral do Sistema

### Pipeline de Dados
```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Fonte de   │      │  Extração    │      │ Armazenamento│      │     API      │
│    Dados     │─────▶│  (Scraper)   │─────▶│    (CSV)     │─────▶│   RESTful    │
│  (Website)   │      │              │      │              │      │              │
└──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘
                                                                           │
                                                                           ▼
                                                                    ┌──────────────┐
                                                                    │  Consumidores│
                                                                    │ (Cientistas  │
                                                                    │   de Dados)  │
                                                                    └──────────────┘
```

## 2. Componentes da Arquitetura

### 2.1 Camada de Ingestão (scripts/scraper.py)

**Responsabilidade**: Extrair dados da fonte externa

**Tecnologias**:
- `requests`: Requisições HTTP
- `BeautifulSoup4`: Parse de HTML
- `csv`: Serialização de dados

**Funcionamento**:
1. Faz requisições paginadas ao site
2. Extrai dados estruturados (título, preço, rating, etc)
3. Aplica delays (0.5s) entre requisições (ética web scraping)
4. Salva em formato CSV padronizado

**Vantagens desta abordagem**:
- Simples e confiável
- Independente da API
- Pode rodar em cronjob para atualização periódica

### 2.2 Camada de Armazenamento (data/books.csv)

**Formato**: CSV (Comma-Separated Values)

**Estrutura**:
```csv
title,price,rating,availability,image_url
"A Light in the Attic",51.77,3,"In stock","https://..."
```

**Por que CSV?**:
- ✅ Simples para desenvolvimento e testes
- ✅ Fácil inspeção manual
- ✅ Compatível com pandas e ferramentas de ML
- ✅ Sem necessidade de servidor de banco de dados

**Limitações**:
- ❌ Não é ideal para produção de alta escala
- ❌ Sem transações ACID
- ❌ Sem índices para buscas rápidas

### 2.3 Camada de Serviço (api/services.py)

**Responsabilidade**: Lógica de negócio e acesso aos dados

**Padrão**: Repository Pattern (simplificado)

**Funções**:
- `load_books_from_csv()`: Carrega dados na memória (startup)
- `get_all_books()`: Retorna todos os livros
- `get_book_by_id()`: Busca por ID
- `search_books()`: Busca por título

**Por que carregar em memória?**:
- ✅ Performance: ~1000 livros = ~1-2 MB RAM
- ✅ Respostas instantâneas (sem I/O)
- ✅ Suficiente para escala pequena/média

### 2.4 Camada de Modelos (api/models.py)

**Tecnologia**: Pydantic

**Modelos**:
```python
Book: id, title, price, rating, availability, image_url
HealthResponse: status, total_books
```

**Benefícios**:
- Validação automática de tipos
- Serialização JSON automática
- Documentação automática (Swagger)

### 2.5 Camada de API (api/main.py)

**Framework**: FastAPI

**Endpoints**:
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/books` | Lista todos |
| GET | `/api/v1/books/search` | Busca por título |
| GET | `/api/v1/books/{id}` | Busca por ID |

**Características**:
- Assíncrono (ASGI)
- Documentação Swagger automática (`/docs`)
- Validação automática de requests/responses
- Tratamento de erros padronizado (HTTPException)

## 3. Escalabilidade - Plano de Evolução

### Fase 1: MVP Atual (Implementado)
```
[CSV] → [API em Memória] → [Cliente]
```
- **Capacidade**: ~1000 livros
- **Latência**: < 50ms
- **Limite**: ~100 req/s

### Fase 2: Banco de Dados (Curto Prazo)
```
[PostgreSQL] → [API com ORM] → [Cliente]
```

**Melhorias**:
- Substituir CSV por PostgreSQL
- Adicionar SQLAlchemy (ORM)
- Habilitar filtros complexos
- Implementar paginação

```python
# Exemplo de migração
@app.get("/api/v1/books")
def list_books(skip: int = 0, limit: int = 100):
    # SELECT * FROM books LIMIT 100 OFFSET 0
    return db.query(Book).offset(skip).limit(limit).all()
```

### Fase 3: Cache e Performance (Médio Prazo)
```
[PostgreSQL] → [Redis Cache] → [API] → [Cliente]
```

**Melhorias**:
- Redis para cache de consultas frequentes
- TTL de 1 hora para dados
- Redução de 90% na latência para buscas repetidas

```python
# Pseudocódigo
def get_book(id):
    # Tenta cache primeiro
    cached = redis.get(f"book:{id}")
    if cached:
        return cached

    # Se não tem no cache, busca no DB
    book = db.get(id)
    redis.set(f"book:{id}", book, ttl=3600)
    return book
```

### Fase 4: Arquitetura Distribuída (Longo Prazo)
```
                          ┌─ [API Instance 1]
[Load Balancer] ─────────┼─ [API Instance 2]
                          └─ [API Instance 3]
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                   [PostgreSQL]          [Redis Cluster]
                   (read replicas)
```

**Melhorias**:
- Horizontal scaling da API
- Load balancer (NGINX)
- Read replicas do PostgreSQL
- Redis Cluster
- CDN para imagens

**Capacidade esperada**:
- ~1M livros
- ~10k req/s
- Latência < 100ms (p99)

## 4. Integração com Machine Learning

### 4.1 Casos de Uso

#### Sistema de Recomendação
```python
# Feature engineering
features = pd.DataFrame([
    {
        'price': book['price'],
        'rating': book['rating'],
        'price_category': 'high' if book['price'] > 40 else 'low'
    }
    for book in api.get_books()
])

# Treinar modelo
from sklearn.neighbors import NearestNeighbors
model = NearestNeighbors(n_neighbors=5)
model.fit(features)

# Recomendações
similar = model.kneighbors([new_book_features])
```

#### Previsão de Disponibilidade
```python
# Classificação: In stock vs Out of stock
X = df[['price', 'rating', 'days_since_published']]
y = df['availability']

model = RandomForestClassifier()
model.fit(X, y)

# API endpoint para predição
@app.post("/api/v1/predict/availability")
def predict(book: BookFeatures):
    prediction = model.predict([[book.price, book.rating, ...]])
    return {"availability": prediction}
```

#### Análise de Sentimento (futuro)
```python
# Se tivermos reviews
from transformers import pipeline

sentiment = pipeline("sentiment-analysis")
book_reviews = api.get_reviews(book_id)

for review in book_reviews:
    sentiment_score = sentiment(review['text'])
```

### 4.2 Pipeline MLOps

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   API       │────▶│  Feature    │────▶│   Model     │────▶│  Prediction │
│  (Dados)    │     │  Store      │     │  Training   │     │   API       │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           │                    ▼
                           │            ┌─────────────┐
                           │            │   Model     │
                           │            │  Registry   │
                           │            └─────────────┘
                           ▼
                    ┌─────────────┐
                    │ Monitoring  │
                    │ (Drift)     │
                    └─────────────┘
```

### 4.3 Expansão da API para ML

**Novos endpoints**:
```python
# Estatísticas agregadas
GET /api/v1/stats/price-distribution
GET /api/v1/stats/rating-distribution

# Features para ML
GET /api/v1/features/books  # Retorna features pré-processadas

# Predições
POST /api/v1/predict/price  # Prever preço de novo livro
POST /api/v1/recommend/{book_id}  # Livros similares
```

## 5. Monitoramento e Observabilidade

### Métricas Importantes

```python
# Logging estruturado
import structlog

logger = structlog.get_logger()

@app.get("/api/v1/books/{id}")
def get_book(id: int):
    logger.info("book_request", book_id=id)
    # ...
```

### Métricas a coletar:
- Request rate (req/s)
- Latência (p50, p95, p99)
- Error rate (%)
- Uptime
- Tamanho do CSV / Número de registros

### Ferramentas (futuro):
- Prometheus + Grafana (métricas)
- ELK Stack (logs)
- Sentry (error tracking)

## 6. Segurança

### Implementado:
- ✅ Validação de entrada (Pydantic)
- ✅ Sem exposição de dados sensíveis

### A implementar:
- Authentication (JWT)
- Rate limiting (por IP/API key)
- CORS configurado corretamente
- HTTPS em produção
- Input sanitization

## 7. Custos e Infraestrutura

### Atual (Gratuito):
- Render Free Tier: $0/mês
- Sem banco de dados

### Futuro (Produção):
```
Componente          | Custo/mês (estimado)
--------------------|---------------------
Render (Web)        | $7/mês
PostgreSQL (Supabase)| $0-25/mês
Redis (Upstash)     | $0-10/mês
CDN (Cloudflare)    | $0/mês
Monitoring (Grafana)| $0-50/mês
--------------------|---------------------
TOTAL               | $7-92/mês
```

## 8. Roadmap Técnico

### Curto Prazo (1-2 meses)
- [ ] Migrar para PostgreSQL
- [ ] Adicionar paginação
- [ ] Implementar testes (pytest)
- [ ] CI/CD (GitHub Actions)

### Médio Prazo (3-6 meses)
- [ ] Redis cache
- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Monitoramento (Prometheus)

### Longo Prazo (6-12 meses)
- [ ] Microserviços (separar scraper)
- [ ] Event streaming (Kafka)
- [ ] Endpoints de ML
- [ ] GraphQL API
