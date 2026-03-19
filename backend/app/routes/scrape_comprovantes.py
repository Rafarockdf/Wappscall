import pdfplumber
import io
import re
from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

from backend.app.services.api_gemini import scrape_images_from_gemini
router = APIRouter()


@router.post("/images/scrape")
async def scrape_image_gemini(file: UploadFile = File(...)):
    dados_nota, dados_cnpj = await scrape_images_from_gemini(file=file)
    return {"status": "sucesso", "dados": dados_nota, "dados_cnpj": dados_cnpj}