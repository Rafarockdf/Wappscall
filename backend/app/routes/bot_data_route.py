from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.app.services.image_pdf_service import save_data_image_pdf_file


router = APIRouter()

@router.post("/uploads")
async def upload_file(file: UploadFile = File(...), telefone: str = Form(...)):
    resultado = await save_data_image_pdf_file(file, telefone)
    if not resultado or (resultado[0] is None and resultado[1] is None):
        raise HTTPException(status_code=500, detail="Erro ao processar o arquivo")
    dados_nota, dados_cnpj = resultado
    return {"status": "sucesso", "dados": dados_nota, "dados_cnpj": dados_cnpj}