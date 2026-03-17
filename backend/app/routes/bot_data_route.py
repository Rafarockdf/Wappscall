from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.app.services.image_pdf_service import save_data_image_pdf_file


router = APIRouter()

@router.post("/uploads")
async def upload_file(file: UploadFile = File(...), telefone: str = Form(...)):
    
    dados_nota, dados_cnpj = await save_data_image_pdf_file(file, telefone)
    
    return {"status": "sucesso", "dados": dados_nota, "dados_cnpj": dados_cnpj}