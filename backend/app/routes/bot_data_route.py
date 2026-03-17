from fastapi import APIRouter, UploadFile, File, Form
import os
import sys

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

from backend.app.services.image_service import save_image_file
from backend.app.services.registra_gasto import RegistraGasto

router = APIRouter()

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    valor: str = Form(None),
    cnpj: str = Form(None),
    data: str = Form(None),
    hora: str = Form(None),
    estabelecimento: str = Form(None),
    pagador: str = Form(None)
):
    await save_image_file(file)
    
    if valor and estabelecimento:
        servico = RegistraGasto(valor, cnpj, data, estabelecimento, pagador)
        gasto_salvo = servico.registrar_gasto()
        
        return {
            "status": "sucesso", 
            "mensagem": "Arquivo e dados gravados!",
            "gasto_id": gasto_salvo.id 
        }
    
    return {"status": "sucesso", "mensagem": "Arquivo gravado, mas dados não fornecidos."}