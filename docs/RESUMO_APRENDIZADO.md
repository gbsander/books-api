# Resumo do Aprendizado - Tech Challenge Books API

## 🎯 O que você construiu

Uma **API RESTful completa** com:
- ✅ Web scraping funcional (1000 livros)
- ✅ Armazenamento em CSV
- ✅ 4 endpoints REST
- ✅ Documentação Swagger automática
- ✅ Pronto para deploy

## 📚 Conceitos Aprendidos

### 1. Web Scraping com Python

**O que faz**: Extrai dados de websites automaticamente

**Bibliotecas usadas**:
```python
requests       # Busca páginas HTML
BeautifulSoup  # Analisa/parse HTML
csv            # Salva em formato tabular
```

**Conceitos importantes**:
- **HTML parsing**: Navegar na árvore de elementos (`find`, `find_all`)
- **Paginação**: Loop para processar múltiplas páginas
- **Ética**: `time.sleep()` para não sobrecarregar servidor
- **Seletores CSS**: `class_='product_pod'` para encontrar elementos

**Exemplo prático**:
```python
# Buscar todos os livros em uma página
books = soup.find_all('article', class_='product_pod')

# Para cada livro, extrair título
for book in books:
    title = book.h3.a['title']  # Navega: book → h3 → a → atributo title
```

### 2. FastAPI - Framework Web Moderno

**O que é**: Framework Python para criar APIs rápidas e modernas

**Por que é bom**:
- Validação automática de dados (Pydantic)
- Documentação automática (Swagger)
- Assíncrono (rápido)
- Type hints nativos

**Conceitos importantes**:

#### Decorators (@)
```python
@app.get("/api/v1/books")  # Define rota GET
def list_books():
    return [...]
```

#### Path Parameters (variáveis na URL)
```python
@app.get("/books/{book_id}")
def get_book(book_id: int):  # FastAPI converte string → int automaticamente
    return book
```

#### Query Parameters (parâmetros após ?)
```python
@app.get("/books/search")
def search(title: Optional[str] = None):  # ?title=python
    return results
```

#### Response Models (validação de saída)
```python
@app.get("/books", response_model=List[Book])
def list_books():
    return books  # FastAPI valida que cada item é um Book
```

### 3. Pydantic - Validação de Dados

**O que faz**: Define estrutura e valida dados automaticamente

```python
class Book(BaseModel):
    id: int         # Deve ser inteiro
    title: str      # Deve ser string
    price: float    # Deve ser número decimal
```

**Benefícios**:
- Converte tipos automaticamente quando possível
- Lança erro se dados estão inválidos
- Gera documentação JSON Schema

### 4. Arquitetura em Camadas

**Separação de responsabilidades**:

```
┌─────────────────┐
│  main.py        │  ← API/Controllers (recebe requests)
│  (Controllers)  │
├─────────────────┤
│  services.py    │  ← Lógica de negócio
│  (Business)     │
├─────────────────┤
│  models.py      │  ← Estrutura de dados
│  (Data Models)  │
├─────────────────┤
│  CSV/Database   │  ← Armazenamento
│  (Storage)      │
└─────────────────┘
```

**Por que é importante**:
- Fácil de testar (cada camada independente)
- Fácil de modificar (trocar CSV por DB só muda `services.py`)
- Código organizado e legível

### 5. REST API - Padrão de Comunicação

**Princípios REST**:

| Método | Uso | Exemplo |
|--------|-----|---------|
| GET | Buscar dados | `GET /books` → Lista todos |
| POST | Criar novo | `POST /books` → Cria livro |
| PUT | Atualizar completo | `PUT /books/1` → Atualiza livro 1 |
| PATCH | Atualizar parcial | `PATCH /books/1` → Atualiza campos |
| DELETE | Deletar | `DELETE /books/1` → Remove livro 1 |

**Códigos HTTP**:
- `200 OK`: Sucesso
- `201 Created`: Recurso criado
- `404 Not Found`: Não encontrado
- `422 Unprocessable Entity`: Dados inválidos
- `500 Internal Server Error`: Erro no servidor

### 6. Pandas - Manipulação de Dados

**O que faz**: Biblioteca poderosa para trabalhar com dados tabulares

```python
import pandas as pd

# Ler CSV
df = pd.read_csv('data/books.csv')

# Converter para lista de dicionários
books = df.to_dict('records')
# [{'title': '...', 'price': 51.77, ...}, ...]

# Filtrar
expensive = df[df['price'] > 50]

# Estatísticas
print(df['price'].mean())  # Preço médio
print(df['rating'].value_counts())  # Contagem de ratings
```

## 🛠️ Comandos Importantes Aprendidos

### Python

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Mac/Linux)
source venv/bin/activate

# Ativar ambiente (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar script
python scripts/scraper.py
```

### FastAPI/Uvicorn

```bash
# Rodar API (modo desenvolvimento)
uvicorn api.main:app --reload

# Rodar em porta específica
uvicorn api.main:app --port 8080

# Rodar em produção
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Git

```bash
# Inicializar repositório
git init

# Adicionar arquivos
git add .

# Commit
git commit -m "Mensagem"

# Conectar ao GitHub
git remote add origin https://github.com/usuario/repo.git

# Enviar
git push -u origin master
```

## 🧠 Conceitos de Programação Aplicados

### 1. List Comprehension
```python
# Transformar lista de dicionários em lista de objetos
books = [Book(**book) for book in books_data]

# É equivalente a:
books = []
for book in books_data:
    books.append(Book(**book))
```

### 2. Unpacking de Dicionário (**)
```python
book_dict = {'id': 1, 'title': 'Python', 'price': 50.0}

# Passa cada chave como argumento nomeado
Book(**book_dict)

# É equivalente a:
Book(id=1, title='Python', price=50.0)
```

### 3. Type Hints
```python
def get_book(book_id: int) -> Optional[Book]:
    # book_id: int = espera receber inteiro
    # -> Optional[Book] = retorna Book ou None
```

### 4. Context Managers (with)
```python
with open('file.csv', 'w') as file:
    # Arquivo fecha automaticamente ao sair do bloco
    file.write(...)
```

### 5. Global Variables
```python
books_data = []  # Global

def load_books():
    global books_data  # Precisa declarar para modificar
    books_data = [...]
```

## 🚀 Próximos Passos no Aprendizado

### Curto Prazo:
1. **Testes automatizados**: Aprenda `pytest`
2. **Banco de dados**: PostgreSQL + SQLAlchemy
3. **Authentication**: JWT tokens
4. **Docker**: Containerizar aplicação

### Médio Prazo:
5. **CI/CD**: GitHub Actions
6. **Monitoring**: Prometheus + Grafana
7. **Cache**: Redis
8. **Message Queue**: RabbitMQ ou Kafka

### Longo Prazo:
9. **Microserviços**: Separar em múltiplos serviços
10. **Kubernetes**: Orquestração de containers
11. **Machine Learning**: Integrar modelos
12. **GraphQL**: Alternativa ao REST

## 📖 Recursos de Estudo

### Documentação Oficial:
- FastAPI: https://fastapi.tiangolo.com/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Pandas: https://pandas.pydata.org/docs/

### Tutoriais:
- Real Python: https://realpython.com/
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- Web Scraping: https://realpython.com/beautiful-soup-web-scraper-python/

### Prática:
- LeetCode (algoritmos): https://leetcode.com/
- HackerRank: https://www.hackerrank.com/
- Kaggle (data science): https://www.kaggle.com/

## 💡 Dicas para Apresentação/Vídeo

### O que destacar:

1. **Pipeline completo**: Ingestão → Armazenamento → API → Consumo
2. **Escalabilidade**: Mostrar plano de evolução (CSV → DB → Cache)
3. **Boas práticas**:
   - Separação de responsabilidades
   - Validação automática
   - Documentação Swagger
   - Deploy automatizado

4. **Demonstração prática**:
   ```bash
   # Mostrar funcionando
   curl https://sua-api.onrender.com/api/v1/health
   curl https://sua-api.onrender.com/api/v1/books/1
   ```

5. **Integração ML** (conceitual):
   - Como cientistas de dados usariam
   - Possíveis modelos (recomendação, previsão)
   - Feature engineering dos dados

### Estrutura do Vídeo (10 min):

1. **Intro (1 min)**: Problema e solução
2. **Arquitetura (2 min)**: Diagrama e pipeline
3. **Demo Scraping (1 min)**: Rodar e mostrar CSV
4. **Demo API (3 min)**: Mostrar endpoints funcionando
5. **Código (2 min)**: Destacar partes importantes
6. **Deploy (1 min)**: API em produção

## ✅ Checklist de Entrega

- [ ] Código no GitHub (público)
- [ ] README completo
- [ ] API deployada (link funcionando)
- [ ] Documentação Swagger acessível
- [ ] Documento de arquitetura
- [ ] Vídeo gravado (3-12 min)
- [ ] CSV com dados (committed ou gerado no build)

---

**Parabéns! 🎉** Você construiu uma aplicação completa do zero, aprendendo conceitos fundamentais de:
- Web scraping
- APIs RESTful
- Arquitetura de software
- Deploy em produção

Este projeto é uma base sólida que você pode expandir e usar em seu portfólio! 🚀
