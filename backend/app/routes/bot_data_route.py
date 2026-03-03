from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.app.services.image_service import save_image_file


router = APIRouter()

@router.post("/uploads")
async def upload_file(file: UploadFile):
    await save_image_file(file)
    
    return {"status": "sucesso"}