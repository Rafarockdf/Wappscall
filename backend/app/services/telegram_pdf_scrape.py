import pdfplumber
import re
from dotenv import load_dotenv
from fastapi import UploadFile
import json
import io
import os
import sys

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.app.services.busca_empresa_scrape_service import consultar_cnpj
load_dotenv()

async def scrape_pdf(pdf_bytes):
    text_content = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content += text + "\n"

    data = {
        "cnpj": None,
        "data": None,
        "valor": None,
        "hora": None,
        "estabelecimento": None,
        "pagador": None
    }

    # CNPJ (Aceita 1 ou 2 dígitos no início, ex: 4.955...)
    cnpj_match = re.search(r'\d{1,2}\.\d{3}\.\d{3}/\d{4}-\d{2}', text)
    if cnpj_match:
        data['cnpj'] = cnpj_match.group(0)

    # Data (dd/mm/aaaa)
    date_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
    if date_match:
        data['data'] = date_match.group(0)

    # Hora (hh:mm:ss ou hh:mm)
    time_match = re.search(r'\d{2}:\d{2}(?::\d{2})?', text)
    if time_match:
        data['hora'] = time_match.group(0)

    # Valor (R$ XX,XX) - Pega o último encontrado (geralmente o total)
    value_pattern = r'(?:R\$\s?)?(\d{1,3}(?:\.\d{3})*,\d{2})'
    values = re.findall(value_pattern, text)
    if values:
        data['valor'] = values[-1]

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for i, line in enumerate(lines):
        line_lower = line.lower()

        if "recebedor" in line_lower or "beneficiário" in line_lower or "destinatário" in line_lower:
            # Se tiver ":" e texto na frente (Ex: "Recebedor: Loja X")
            if ":" in line and len(line) > 12: 
                parts = line.split(":", 1)
                if len(parts) > 1 and len(parts[1].strip()) > 2:
                    data['estabelecimento'] = parts[1].strip()
            # Senão, pega a linha de baixo (Ex: "Recebedor" [enter] "Loja X")
            elif i + 1 < len(lines):
                data['estabelecimento'] = lines[i + 1]

        # Busca por PAGADOR / CLIENTE
        if "pagador" in line_lower or "cliente" in line_lower:
            if ":" in line and len(line) > 10:
                parts = line.split(":", 1)
                if len(parts) > 1 and len(parts[1].strip()) > 2:
                    data['pagador'] = parts[1].strip()
            elif i + 1 < len(lines):
                data['pagador'] = lines[i + 1]

    dados_pagamento = {
        "valor": data['valor'],
        "data": data['data'],
        "hora": data['hora'],
        "cnpj": data['cnpj']
    }

    cnpj_tratado = dados_pagamento['cnpj'].replace(".", "").replace("/", "").replace("-", "") if dados_pagamento['cnpj'] else None
    print(f"CNPJ extraído do PDF: {dados_pagamento['cnpj']} -> Tratado: {cnpj_tratado}")
    dados_cnpj = await consultar_cnpj(str(cnpj_tratado))
    print(f"Dados da empresa consultados: {dados_cnpj}")

    return dados_pagamento, dados_cnpj