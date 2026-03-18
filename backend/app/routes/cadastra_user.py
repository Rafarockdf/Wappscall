import pdfplumber
import io
import re
from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
#from backend.app.services.email_scrape_service import scrape_emails_from_gmail
from backend.app.services.funcionario_service import FuncionarioService
from imap_tools import MailBox, AND
router = APIRouter()


@router.post("/cadastra_user")
async def cadastra_user(nome: str = Form(...), cargo: str = Form(...), salario: str = Form(...), data_contratacao: str = Form(...),telefone: str = Form(...)):
    print(f"Recebido: nome={nome}, cargo={cargo}, salario={salario}, telefone={telefone}, data_contratacao={data_contratacao}")
    
    salario_float = float(salario)
    
    funcionario_service = FuncionarioService()
    json = funcionario_service.cadastrar_funcionario(nome, cargo, salario_float, telefone, data_contratacao)
    return {"status": "sucesso", "dados": json}