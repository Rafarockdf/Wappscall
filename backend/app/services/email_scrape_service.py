import pdfplumber
import io
import re
from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from imap_tools import MailBox, AND
from dotenv import load_dotenv
from backend.app.services.busca_empresa_scrape_service import consultar_cnpj

load_dotenv()
usuario = os.getenv("EMAIL_USER")
senha = os.getenv("EMAIL_TOKEN")
print(f"Usuário: {usuario}")
print(f"Senha: {senha}")
async def scrape_emails_from_gmail():
    with MailBox("imap.gmail.com").login(usuario, senha) as meu_email:
            compr_emails = meu_email.fetch(AND(subject="Comprovante de pagamento", seen=False), mark_seen=False)

            print("🔍 Iniciando busca de comprovantes...\n")

            for email in compr_emails:
                resultado_anexos = []

                if len(email.attachments) > 0:
                    for anexo in email.attachments:
                        if anexo.filename.lower().endswith(".pdf"):

                            pdf_data = io.BytesIO(anexo.payload)
                            
                            try:
                                with pdfplumber.open(pdf_data) as pdf:

                                    texto = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

                                empresa_match = re.search(r"Recebemos de (.*?),", texto)
                                empresa = empresa_match.group(1).strip() if empresa_match else "Não encontrado"
                                
                                cnpj_match = re.search(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto)
                                cnpj = cnpj_match.group(0) if cnpj_match else "Não encontrado"
                                
                                data_match = re.search(r"(\d{2}/\d{2}/\d{4})", texto)
                                data = data_match.group(0) if data_match else "Não encontrada"
                                
                                valor_match = re.search(r"VALOR TOTAL DA NOTA\s+([\d.]+,\d{2})", texto, re.IGNORECASE)
                                if not valor_match:
                                    valor_match = re.search(r"R\$\s?([\d.]+,\d{2})", texto)
                                
                                valor = valor_match.group(1) if valor_match else "Não encontrado"

                                resultado_anexos.append({
                                    "arquivo": anexo.filename,
                                    "empresa": empresa,
                                    "cnpj": cnpj,
                                    "data": data,
                                    "valor": valor
                                })
                            except Exception as e:
                                print(f"❌ Erro ao ler o arquivo {anexo.filename}: {e}")

                if resultado_anexos:
                    print("="*50)
                    print(f"E-MAIL ENCONTRADO")
                    print(f"De:      {email.from_}")
                    print(f"Assunto: {email.subject}")
                    print(f"Data:    {email.date}")
                    print("-" * 50)
                    cnpj_tratado = resultado_anexos[0]["cnpj"]
                    print(f"Empresa: {resultado_anexos[0]['empresa']}")
                    print(f"CNPJ:    {resultado_anexos[0]['cnpj']}")
                    print(f"CNPJTTT:    {cnpj_tratado}")
                    dados_cnpj = await consultar_cnpj(str(cnpj_tratado))
                    return dados_cnpj
                else:
                    print(f"ℹ️ E-mail de '{email.from_}' processado, mas nenhum anexo PDF válido foi encontrado.")

            print("✅ Processamento finalizado.")