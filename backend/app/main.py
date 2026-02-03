import os
import sys

from backend.app.routes import bot_data_route

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)


from fastapi import FastAPI, Depends, status, APIRouter
from typing import List
from sqlalchemy.orm import Session
# Certifique-se de que estes arquivos existem no seu projeto
#from schemas import Mensagem
#from backend.database.models import models
#from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
# Cria as tabelas no banco de dados
#models.Base.metadata.create_all(bind=engine)
from backend.app.routes import bot_data_route


app = FastAPI()


app.include_router(bot_data_route.router, prefix="/uploads")

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


# Cria o roteador
router = APIRouter()

@router.get("/itens")
def listar_itens():
    return {"mensagem": "Lista de itens do arquivo de rotas"}

@app.get("/")
async def root():
    return {"message": "Hello World"}