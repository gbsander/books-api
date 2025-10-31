# Guia de Deploy - Books API

## 📦 Deploy no Render (Recomendado - Gratuito)

### Passo 1: Preparar repositório Git

```bash
# Se ainda não inicializou o git
git init
git add .
git commit -m "Implementação da Books API com web scraping"

# Subir para GitHub
git remote add origin https://github.com/seu-usuario/books-api.git
git push -u origin master
```

### Passo 2: Criar conta no Render

1. Acesse [render.com](https://render.com)
2. Faça login com GitHub
3. Clique em **"New +"** → **"Web Service"**

### Passo 3: Configurar o Web Service

**Configurações**:
- **Repository**: Selecione seu repositório
- **Name**: `books-api` (ou outro nome)
- **Environment**: `Python 3`
- **Region**: Escolha a mais próxima
- **Branch**: `master` (ou `main`)
- **Build Command**: `./build.sh`
- **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- **Plan**: `Free`

### Passo 4: Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o build (3-5 minutos)
3. Sua API estará disponível em: `https://seu-app.onrender.com`

### Passo 5: Testar

```bash
# Substituir pela sua URL do Render
curl https://seu-app.onrender.com/api/v1/health

# Acessar documentação
# Abrir no navegador: https://seu-app.onrender.com/docs
```

## 🚀 Deploy no Fly.io (Alternativa)

### Passo 1: Instalar Fly CLI

```bash
# Mac
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Passo 2: Login

```bash
fly auth login
```

### Passo 3: Criar arquivo fly.toml

```toml
app = "books-api"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Passo 4: Deploy

```bash
# Primeira vez
fly launch

# Deploys subsequentes
fly deploy
```

## 🐳 Deploy com Docker (Avançado)

### Criar Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Executar scraping
RUN python scripts/scraper.py

# Expor porta
EXPOSE 8000

# Comando para rodar
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build e Run

```bash
# Build
docker build -t books-api .

# Run
docker run -p 8000:8000 books-api
```

### Deploy no Railway

1. Instale Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Deploy: `railway up`

## ☁️ Deploy no Vercel (Serverless)

**Nota**: Vercel é otimizado para Next.js, mas funciona com FastAPI usando adaptador

### Criar vercel.json

```json
{
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/main.py"
    }
  ]
}
```

### Deploy

```bash
npm install -g vercel
vercel --prod
```

## 🔍 Verificação Pós-Deploy

### Checklist:

- [ ] API está respondendo em `/api/v1/health`
- [ ] Documentação está acessível em `/docs`
- [ ] Todos os endpoints funcionam corretamente
- [ ] Logs não mostram erros críticos
- [ ] Dados do CSV foram carregados (total_books > 0)

### Testes:

```bash
# Substituir pela URL do seu deploy
API_URL="https://seu-app.onrender.com"

# Health
curl "$API_URL/api/v1/health"

# Listar livros
curl "$API_URL/api/v1/books" | head -100

# Buscar por ID
curl "$API_URL/api/v1/books/1"

# Buscar por título
curl "$API_URL/api/v1/books/search?title=python"
```

## 📊 Monitoramento

### Logs no Render

```bash
# Via dashboard: render.com → seu serviço → Logs
```

### Métricas importantes:

- **Response time**: < 500ms
- **Error rate**: < 1%
- **Uptime**: > 99%

## 🐛 Troubleshooting

### Erro: "Application failed to start"

**Solução**:
1. Verifique logs de build
2. Confirme que `build.sh` tem permissão de execução: `chmod +x build.sh`
3. Teste localmente: `./build.sh && uvicorn api.main:app`

### Erro: "Module not found"

**Solução**:
1. Verifique `requirements.txt`
2. Confirme que build command instala dependências
3. Teste localmente em venv limpo

### Erro: "Port already in use"

**Solução**:
- Em deploy: Usar `$PORT` (variável de ambiente)
- Local: `lsof -ti:8000 | xargs kill`

### API lenta

**Soluções**:
1. Verificar se CSV está sendo carregado no startup (não a cada request)
2. Considerar adicionar cache
3. Otimizar buscas com índices (se migrar para DB)

## 🔐 Variáveis de Ambiente (Futuro)

Para configurações sensíveis:

```bash
# No Render: Settings → Environment Variables
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
SECRET_KEY=sua-chave-secreta
API_KEY=sua-api-key
```

```python
# No código
import os

DATABASE_URL = os.getenv("DATABASE_URL")
```

## 📈 Próximos Passos

1. Configurar domínio customizado
2. Adicionar SSL (automático no Render/Fly)
3. Configurar CI/CD (GitHub Actions)
4. Implementar monitoramento (UptimeRobot gratuito)
5. Adicionar analytics

---

Boa sorte com o deploy! 🚀
