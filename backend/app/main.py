import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.app.routes import bot_data_route

from backend.app.services.image_service import save_image_file

from fastapi import FastAPI, Depends, status, APIRouter, UploadFile
from typing import List
#from sqlalchemy.orm import Session
# Certifique-se de que estes arquivos existem no seu projeto
#from schemas import Mensagem
#from backend.database.models import models
#from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
# Cria as tabelas no banco de dados
#models.Base.metadata.create_all(bind=engine)
from backend.app.routes import gastos_route


app = FastAPI()


app.include_router(bot_data_route.router, prefix="/uploads")
app.include_router(gastos_route.router)

# Configuração para permitir que o React converse com o FastAPI
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
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
