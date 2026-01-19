from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

router = APIRouter(prefix="/uploads", tags=["Imagens"])

@router.post("/imagem")
async def salvar_imagem(
    user_id: str = Form(...), 
    file: UploadFile = File(...)
):
    # Definir caminho onde a imagem será salva
    upload_dir = "static/images"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    # Salvar o arquivo fisicamente no servidor
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Aqui você inseriria no Banco de Dados usando sua lógica de Service/Model
    # Exemplo fictício: db.save_image_info(user_id, file_path)

    return {
        "status": "sucesso",
        "filename": file.filename,
        "url": f"http://suaapi.com/static/images/{file.filename}"
    }