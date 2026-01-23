from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

router = APIRouter()

@router.post("/uploads")
async def upload_file(file: UploadFile, amount: float):
    # 1. Chama função para salvar fisicamente no storage/
    #file_path = storage_service.save_file(file) 
    
    # 2. Chama função do database/ para registrar
    #repository.save_expense_to_db(db, {"amount": amount}, file_path)
    
    return {"status": "sucesso"}