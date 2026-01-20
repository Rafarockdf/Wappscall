# 📐 Arquitetura Recomendada - Projeto Wappscal

> Guia passo a passo para refatorar e organizar o projeto seguindo boas práticas

---

## 📁 Estrutura de Diretórios Completa

```
Configs/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app principal
│   │   ├── config.py                  # Configurações (NEW)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── bot_data.py
│   │   ├── services/
│   │   │   ├── __init__.py            # (NEW)
│   │   │   └── [services specificos]
│   │   ├── schemas/                   # (NEW)
│   │   │   ├── __init__.py
│   │   │   └── mensagem.py
│   │   └── exceptions/                # (NEW)
│   │       ├── __init__.py
│   │       └── custom_exceptions.py
│   ├── database/
│   │   ├── __init__.py                # (NEW)
│   │   ├── base.py                    # (NEW) Base class para models
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── models/
│   │   │   ├── __init__.py            # (NEW)
│   │   │   └── [models database]
│   │   └── session.py                 # (NEW) Gerenciamento de sessões
│   ├── tests/                         # (NEW)
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_routes/
│   │   └── test_services/
│   ├── requirements.txt
│   ├── .env.example                   # (NEW) Template de variáveis
│   └── pytest.ini                     # (NEW) Configuração de testes
│
├── bot/
│   ├── __init__.py                    # (NEW)
│   ├── main.py                        # Entrada principal do bot
│   ├── config.py                      # (NEW) Configurações do bot
│   ├── handlers/
│   │   ├── __init__.py                # (NEW)
│   │   └── [handlers specificos]
│   ├── services/                      # (NEW)
│   │   ├── __init__.py
│   │   └── [services do bot]
│   ├── utils/
│   │   ├── __init__.py                # (NEW)
│   │   └── [utilitários]
│   ├── tests/                         # (NEW)
│   │   ├── __init__.py
│   │   └── test_handlers/
│   ├── requirements.txt
│   ├── .env.example                   # (NEW)
│   └── pytest.ini                     # (NEW)
│
├── shared/                            # (NEW) Código compartilhado
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── base_models.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── constants.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── base_exceptions.py
│   └── validators/
│       ├── __init__.py
│       └── validations.py
│
├── docker/                            # (NEW) Arquivos Docker
│   ├── Dockerfile.backend
│   ├── Dockerfile.bot
│   └── .dockerignore
│
├── .github/                           # (NEW) Configuração GitHub
│   └── workflows/
│       ├── tests.yml
│       └── deploy.yml
│
├── doc/
│   └── EstruturaProjeto.md
│
├── .env                               # Variáveis de ambiente (NÃO commitar)
├── .env.example                       # (NEW) Template (commitar)
├── .gitignore                         # (NEW)
├── docker-compose.yml                 # (NEW) Orquestração containers
├── pyproject.toml                     # (NEW) Configuração do projeto
├── pytest.ini                         # (NEW) Configuração global de testes
├── README.md
└── ARQUITETURA_RECOMENDADA.md        # Este arquivo
```

---

## 🎯 Passo a Passo de Implementação

### **Fase 1: Estrutura de Diretórios**

#### Passo 1.1: Criar arquivos `__init__.py`
```bash
# No PowerShell
New-Item -Path "backend/app" -Name "__init__.py" -Force
New-Item -Path "backend/app/routes" -Name "__init__.py" -Force
New-Item -Path "backend/app/services" -Name "__init__.py" -Force
New-Item -Path "backend/app/schemas" -Name "__init__.py" -Force
New-Item -Path "backend/app/exceptions" -Name "__init__.py" -Force
New-Item -Path "backend/database" -Name "__init__.py" -Force
New-Item -Path "backend/database/models" -Name "__init__.py" -Force
New-Item -Path "backend/tests" -Name "__init__.py" -Force
New-Item -Path "bot" -Name "__init__.py" -Force
New-Item -Path "bot/handlers" -Name "__init__.py" -Force
New-Item -Path "bot/services" -Name "__init__.py" -Force
New-Item -Path "bot/utils" -Name "__init__.py" -Force
New-Item -Path "bot/tests" -Name "__init__.py" -Force
New-Item -Path "shared" -Name "__init__.py" -Force
New-Item -Path "shared/models" -Name "__init__.py" -Force
New-Item -Path "shared/utils" -Name "__init__.py" -Force
New-Item -Path "shared/exceptions" -Name "__init__.py" -Force
New-Item -Path "shared/validators" -Name "__init__.py" -Force
```

#### Passo 1.2: Criar novos diretórios
```bash
mkdir docker
mkdir ".github/workflows"
mkdir "backend/tests/test_routes"
mkdir "backend/tests/test_services"
mkdir "bot/tests/test_handlers"
```

---

### **Fase 2: Arquivos de Configuração**

#### Passo 2.1: `.env.example` (Backend)
```
# Database
DATABASE_URL=postgresql://user:password@localhost/wappscal_db

# FastAPI
DEBUG=True
API_HOST=localhost
API_PORT=8000
API_TITLE=Wappscal API

# CORS
FRONTEND_URL=http://localhost:3001

# Bot
BOT_TOKEN=your_token_here
BOT_WEBHOOK_URL=http://localhost:8000/webhook
```

#### Passo 2.2: `.env.example` (Bot)
```
# WhatsApp
WHATSAPP_TOKEN=your_token_here
WHATSAPP_PHONE_ID=your_phone_id

# API Backend
API_URL=http://localhost:8000
API_KEY=your_api_key

# Logging
LOG_LEVEL=INFO
```

#### Passo 2.3: `.gitignore`
```
# Environment
.env
.env.local
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

#### Passo 2.4: `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "wappscal"
version = "0.1.0"
description = "WhatsApp Bot + API Backend"
readme = "README.md"
requires-python = ">=3.9"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "flake8>=6.0",
    "isort>=5.0",
]

[tool.black]
line-length = 100
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 100

[tool.pytest.ini_options]
testpaths = ["backend/tests", "bot/tests"]
addopts = "-v --cov"
```

#### Passo 2.5: `docker-compose.yml`
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: wappscal_db
      POSTGRES_USER: wappscal
      POSTGRES_PASSWORD: wappscal_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://wappscal:wappscal_password@postgres/wappscal_db
    depends_on:
      - postgres
    volumes:
      - ./backend:/app/backend

  bot:
    build:
      context: .
      dockerfile: docker/Dockerfile.bot
    environment:
      API_URL: http://backend:8000
    depends_on:
      - backend
    volumes:
      - ./bot:/app/bot

volumes:
  postgres_data:
```

#### Passo 2.6: `docker/Dockerfile.backend`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Passo 2.7: `docker/Dockerfile.bot`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ .
COPY shared/ ../shared/

CMD ["python", "main.py"]
```

---

### **Fase 3: Estrutura de Código**

#### Passo 3.1: `backend/app/config.py` (NEW)
```python
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DEBUG: bool = True
    API_TITLE: str = "Wappscal API"
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/wappscal"
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3001"
    
    # Bot
    BOT_TOKEN: str = ""
    BOT_WEBHOOK_URL: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

#### Passo 3.2: `backend/database/session.py` (NEW)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.database.config.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Passo 3.3: `backend/database/__init__.py` (NEW)
```python
from backend.database.session import engine, SessionLocal, get_db
from backend.database.models import Base

__all__ = ["engine", "SessionLocal", "get_db", "Base"]
```

#### Passo 3.4: `backend/app/schemas/mensagem.py` (NEW)
```python
from pydantic import BaseModel
from typing import Optional

class MensagemBase(BaseModel):
    conteudo: str
    remetente: str

class MensagemCreate(MensagemBase):
    pass

class Mensagem(MensagemBase):
    id: int
    criada_em: str
    
    class Config:
        from_attributes = True
```

#### Passo 3.5: `backend/app/exceptions/custom_exceptions.py` (NEW)
```python
class BaseException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class MensagemNaoEncontrada(BaseException):
    def __init__(self):
        super().__init__("Mensagem não encontrada", 404)

class DadosInvalidos(BaseException):
    def __init__(self, detalhe: str):
        super().__init__(f"Dados inválidos: {detalhe}", 422)
```

#### Passo 3.6: `backend/app/services/mensagem_service.py` (NEW)
```python
from sqlalchemy.orm import Session
from backend.database.models import MensagemModel
from backend.app.schemas.mensagem import MensagemCreate

class MensagemService:
    @staticmethod
    def criar_mensagem(db: Session, mensagem: MensagemCreate) -> MensagemModel:
        db_mensagem = MensagemModel(**mensagem.dict())
        db.add(db_mensagem)
        db.commit()
        db.refresh(db_mensagem)
        return db_mensagem
    
    @staticmethod
    def obter_todas_mensagens(db: Session) -> list[MensagemModel]:
        return db.query(MensagemModel).all()
    
    @staticmethod
    def obter_mensagem_por_id(db: Session, mensagem_id: int) -> MensagemModel:
        return db.query(MensagemModel).filter(MensagemModel.id == mensagem_id).first()
```

#### Passo 3.7: `bot/config.py` (NEW)
```python
import os
from dotenv import load_dotenv

load_dotenv()

class BotConfig:
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
    WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

#### Passo 3.8: `shared/utils/helpers.py` (NEW)
```python
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def log_info(mensagem: str):
    logger.info(mensagem)

def log_error(mensagem: str):
    logger.error(mensagem)

def obter_timestamp() -> str:
    return datetime.now().isoformat()
```

#### Passo 3.9: `shared/models/base_models.py` (NEW)
```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

---

### **Fase 4: Testes**

#### Passo 4.1: `backend/pytest.ini`
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers
markers =
    unit: unit tests
    integration: integration tests
```

#### Passo 4.2: `backend/tests/conftest.py`
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.base import Base
from backend.app.main import app
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    return TestClient(app)
```

#### Passo 4.3: `backend/tests/test_routes/test_bot_data.py` (NEW)
```python
import pytest
from fastapi.testclient import TestClient

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

---

### **Fase 5: Atualizar main.py do Backend**

#### `backend/app/main.py` (ATUALIZADO)
```python
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Adicionar caminho do projeto
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

from backend.app.config import settings
from backend.database import engine, Base
from backend.app.routes import bot_data
from backend.app import schemas, exceptions

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version="0.1.0",
    debug=settings.DEBUG
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar rotas
app.include_router(bot_data.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT
    )
```

---

## ✅ Checklist de Implementação

- [ ] **Fase 1**: Criar todos os `__init__.py`
- [ ] **Fase 1**: Criar novos diretórios
- [ ] **Fase 2**: Criar arquivos `.env.example`
- [ ] **Fase 2**: Criar `.gitignore`
- [ ] **Fase 2**: Criar `pyproject.toml`
- [ ] **Fase 2**: Criar `docker-compose.yml`
- [ ] **Fase 2**: Criar `docker/Dockerfile.backend`
- [ ] **Fase 2**: Criar `docker/Dockerfile.bot`
- [ ] **Fase 3**: Criar `backend/app/config.py`
- [ ] **Fase 3**: Criar `backend/database/session.py`
- [ ] **Fase 3**: Criar `backend/database/__init__.py`
- [ ] **Fase 3**: Criar `backend/app/schemas/`
- [ ] **Fase 3**: Criar `backend/app/exceptions/`
- [ ] **Fase 3**: Criar `backend/app/services/`
- [ ] **Fase 3**: Criar `bot/config.py`
- [ ] **Fase 3**: Criar `shared/` com modelos e utilidades
- [ ] **Fase 4**: Criar estrutura de testes
- [ ] **Fase 5**: Atualizar `backend/app/main.py`

---

## 📚 Próximos Passos

1. **Implementar fase por fase** conforme este documento
2. **Testar cada mudança** para garantir compatibilidade
3. **Adicionar CI/CD** com GitHub Actions
4. **Documentar APIs** com Swagger (FastAPI já inclui)
5. **Implementar logging** centralizado

---

## 🔗 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
