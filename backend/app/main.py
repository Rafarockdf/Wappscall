import os
import sys

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)


from fastapi import FastAPI, Depends, status
from typing import List
from sqlalchemy.orm import Session
# Certifique-se de que estes arquivos existem no seu projeto
#from schemas import Mensagem
from backend.database.models import models
#from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# Cria as tabelas no banco de dados
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração para permitir que o React converse com o FastAPI
origins = [
    "http://localhost:3001", # Porta padrão do React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}