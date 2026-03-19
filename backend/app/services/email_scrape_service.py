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
from backend.app.services.funcionario_service import FuncionarioService
from backend.app.services.gastos_service_crud import GastosService
from datetime import datetime

load_dotenv()
usuario = os.getenv("EMAIL_USER")
senha = os.getenv("EMAIL_TOKEN")
print(f"Usuário: {usuario}")
print(f"Senha: {senha}")
funcionario_service = FuncionarioService()
gastos_service = GastosService()
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
                    
                    dados = resultado_anexos[0]

                    valor = dados.get("valor", 0)
                    valor = float(valor.replace(".", "").replace(",", ".")) if valor else 0

                    cnpj = dados.get("cnpj", "Desconecido")
                    cnpj_tratado = re.sub(r"\D", "", cnpj)

                    data_str = dados.get("data", "Desconecido")

                    if data_str != "Desconecido":
                        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
                    else:
                        data_obj = None

                    dados_cnpj = await consultar_cnpj(cnpj_tratado)
                    dados_cnpj = dados_cnpj if isinstance(dados_cnpj, dict) else {}

                    razao_social = dados_cnpj.get("razao_social", "Desconecido")
                    estabelecimento = dados_cnpj.get("nome_fantasia", "Desconecido")

                    cnae_principal = dados_cnpj.get("cnae_principal") or {}
                    categoria = cnae_principal.get("descricao", "Desconhecido") if isinstance(cnae_principal, dict) else str(cnae_principal)

                    telefone = email.from_

                    func_id = await funcionario_service.get_funcionario_id_by_telefone(telefone)

                    gastos_service.cadastrar_gasto(
                        funcionario_id=func_id,
                        motivo="Consumo",
                        descricao=f"Comprovante recebido por e-mail: {dados.get('arquivo')}",
                        valor=valor,
                        cnpj=cnpj,
                        data=data_obj,
                        empresa=estabelecimento,
                        razao_social=razao_social,
                        ramo_atividade=categoria,
                        categoria=categoria,
                        arquivo_extracao=None,
                        tipo_gasto="Dinheiro Funcionário"
                    )
                    
                    return resultado_anexos[0], dados_cnpj
                    
                else:
                    print(f"ℹ️ E-mail de '{email.from_}' processado, mas nenhum anexo PDF válido foi encontrado.")
