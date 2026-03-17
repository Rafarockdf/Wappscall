import pdfplumber
import io
import re
from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.app.services.email_scrape_service import scrape_emails_from_gmail
from imap_tools import MailBox, AND
router = APIRouter()


@router.get("/emails/scrape")
async def scrape_emails():
    dados_nota, dados_cnpj = await scrape_emails_from_gmail()
    return {"status": "sucesso", "dados": dados_nota, "dados_cnpj": dados_cnpj}