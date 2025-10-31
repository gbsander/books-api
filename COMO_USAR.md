# 🚀 Como Usar Este Projeto - Guia Rápido

## ⚡ Início Rápido (3 comandos)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar scraping (se ainda não tem o CSV)
python scripts/scraper.py

# 3. Rodar API
uvicorn api.main:app --reload
```

Pronto! API rodando em `http://localhost:8000`

Acesse a documentação interativa: `http://localhost:8000/docs`

---

## 📝 Testar os Endpoints

### No terminal:
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Listar todos os livros
curl http://localhost:8000/api/v1/books

# Buscar livro por ID
curl http://localhost:8000/api/v1/books/5

# Buscar por título
curl "http://localhost:8000/api/v1/books/search?title=python"

# Listar categorias
curl http://localhost:8000/api/v1/categories
```

### No navegador:
- Documentação Swagger: `http://localhost:8000/docs`
- Teste direto pela interface gráfica

---

## 📦 Estrutura do Que Foi Criado

```
tc1_/
├── 📄 README.md                    ← Documentação principal
├── 📄 COMO_USAR.md                ← Este arquivo
├── 📄 requirements.txt            ← Dependências Python
├── 📄 .gitignore                  ← Arquivos ignorados pelo Git
│
├── 🗂️  scripts/
│   └── scraper.py                 ← Web scraper (extrai dados)
│
├── 🗂️  api/
│   ├── __init__.py
│   ├── main.py                    ← Aplicação FastAPI (endpoints)
│   ├── models.py                  ← Modelos Pydantic (validação)
│   └── services.py                ← Lógica de negócio
│
├── 🗂️  data/
│   └── books.csv                  ← 1000 livros extraídos
│
├── 🗂️  docs/
│   ├── ARQUITETURA.md             ← Plano arquitetural
│   ├── DEPLOY.md                  ← Guia de deploy
│   ├── ENDPOINTS.md               ← Documentação da API
│   └── RESUMO_APRENDIZADO.md      ← Conceitos e aprendizados
│
└── 🗂️  Arquivos de Deploy
    ├── Procfile                   ← Heroku
    ├── render.yaml                ← Render
    └── build.sh                   ← Script de build
```

---

## 🎯 O Que Cada Arquivo Faz

### scripts/scraper.py
- **O que faz**: Acessa books.toscrape.com e extrai dados de todos os livros
- **Como usar**: `python scripts/scraper.py`
- **Resultado**: Cria `data/books.csv` com 1000 livros

### api/main.py
- **O que faz**: Servidor FastAPI com 5 endpoints REST
- **Como usar**: `uvicorn api.main:app --reload`
- **Acesso**: `http://localhost:8000`

### api/models.py
- **O que faz**: Define estrutura dos dados (Book, HealthResponse)
- **Tecnologia**: Pydantic (validação automática)

### api/services.py
- **O que faz**: Funções de negócio (carregar CSV, buscar livros)
- **Pattern**: Repository Pattern simplificado

---

## 🐛 Resolução de Problemas

### Erro: "Module not found"
```bash
# Certifique-se que instalou as dependências
pip install -r requirements.txt
```

### Erro: "Port 8000 already in use"
```bash
# Matar processo na porta 8000
lsof -ti:8000 | xargs kill

# Ou usar outra porta
uvicorn api.main:app --reload --port 8080
```

### Erro: "FileNotFoundError: data/books.csv"
```bash
# Execute o scraper primeiro
python scripts/scraper.py
```

### API não carrega dados
- Verifique se `data/books.csv` existe
- Verifique os logs no terminal onde rodou `uvicorn`
- Acesse `/api/v1/health` para ver quantos livros foram carregados

---

## 📚 Próximos Passos

### 1. Commitar no Git
```bash
git init
git add .
git commit -m "Implementação completa da Books API - Tech Challenge"
```

### 2. Subir no GitHub
```bash
# Crie um repositório no GitHub primeiro, depois:
git remote add origin https://github.com/SEU-USUARIO/books-api.git
git branch -M main
git push -u origin main
```

### 3. Deploy no Render (Gratuito)
1. Acesse [render.com](https://render.com)
2. Faça login com GitHub
3. Clique em "New +" → "Web Service"
4. Selecione seu repositório
5. Configure:
   - **Build Command**: `./build.sh`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
6. Clique em "Create Web Service"
7. Aguarde 3-5 minutos
8. Sua API estará online! 🎉

### 4. Gravar Vídeo (3-12 minutos)

**Estrutura sugerida**:
1. **Intro (1 min)**: Apresentação do problema e solução
2. **Arquitetura (2 min)**: Mostrar `docs/ARQUITETURA.md` com diagrama
3. **Demo Scraping (1 min)**: Rodar `python scripts/scraper.py`
4. **Demo API (3 min)**:
   - Mostrar Swagger (`/docs`)
   - Testar endpoints
   - Mostrar API em produção (Render)
5. **Código (2 min)**: Destacar partes importantes do código
6. **Escalabilidade (1 min)**: Falar sobre melhorias futuras

---

## 📖 Documentação Completa

Leia os arquivos na pasta `docs/` para entender melhor:

- **ARQUITETURA.md**: Como o sistema foi projetado e como escalar
- **DEPLOY.md**: Guia detalhado de deploy em várias plataformas
- **ENDPOINTS.md**: Documentação completa da API com exemplos
- **RESUMO_APRENDIZADO.md**: Conceitos aprendidos e explicações

---

## ✅ Checklist de Entrega

- [ ] ✅ Web scraping funcional (1000 livros)
- [ ] ✅ CSV gerado e commitado
- [ ] ✅ API com 5 endpoints obrigatórios
- [ ] ✅ Documentação Swagger acessível
- [ ] ✅ README completo
- [ ] ✅ Plano arquitetural (docs/ARQUITETURA.md)
- [ ] ⏳ Código no GitHub (público)
- [ ] ⏳ API deployada (Render/Heroku/etc)
- [ ] ⏳ Vídeo gravado (3-12 min)

---

## 💡 Dicas Extras

### Melhorar o README para portfólio:
- Adicione seu nome
- Adicione link do GitHub/LinkedIn
- Adicione badges (Python, FastAPI, etc)
- Adicione screenshots da API funcionando

### Destacar no vídeo:
- **Boas práticas**: Separação em camadas, validação automática
- **Ética**: Delays no scraping
- **Documentação**: Swagger automático
- **Escalabilidade**: Plano de evolução CSV → DB → Cache

---

## 🎉 Parabéns!

Você construiu uma aplicação completa end-to-end incluindo:
- ✅ Web scraping ético
- ✅ API RESTful profissional
- ✅ Documentação completa
- ✅ Pronto para deploy
- ✅ Plano de escalabilidade

Este projeto demonstra conhecimentos em:
- Python
- Web Scraping
- APIs REST
- FastAPI
- Arquitetura de Software
- DevOps (Deploy)

**Boa sorte no Tech Challenge! 🚀**
