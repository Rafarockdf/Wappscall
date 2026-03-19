import os
import sys
from PIL import Image
from fastapi import UploadFile
from dotenv import load_dotenv
import io
import shutil
from pathlib import Path
from datetime import datetime
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.app.services.data_hora_atual import obter_data_hora_atual
from backend.app.services.api_gemini import scrape_images_from_gemini
from backend.app.services.telegram_pdf_scrape import scrape_pdf
from backend.app.services.gastos_service_crud import GastosService
from backend.app.services.funcionario_service import FuncionarioService
load_dotenv()

gastos_service = GastosService()
funcionario_service = FuncionarioService()

async def save_data_image_pdf_file(file: UploadFile, telefone: str):
    pasta_destino = os.getenv('CAMINHO_ARQUIVOS')
    print(file.content_type)
    print(telefone)
    # 2. Criar a pasta se ela não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    if file.content_type == 'image/jpeg':
        try:
            pasta_destino_img = pasta_destino + '/img'
            # 3. Ler o conteúdo do UploadFile
            # Usamos io.BytesIO para que a PIL possa ler os bytes vindos da memória
            conteudo = await file.read()
            img = Image.open(io.BytesIO(conteudo))

            # 4. Definir o caminho final
            # Usamos o nome original do arquivo ou um nome padrão
            data_hora_atual = obter_data_hora_atual()
            
            nome_arquivo = f"comprovante_{telefone}_{data_hora_atual}_{file.filename}" 
            caminho_final = os.path.join(pasta_destino_img, nome_arquivo)

            # 5. Salvar a imagem
            # Se quiser manter o formato original, pode usar img.format
            img.save(caminho_final)
            print(f"Imagem salva com sucesso em: {caminho_final}")
            await file.seek(0) # Volta para o início do arquivo para que possa ser lido novamente
            dados_pagamento, dados_cnpj = await scrape_images_from_gemini(file=file)
            print(f"Dados extraídos da imagem: {dados_pagamento}")
            print(f"Dados da empresa consultados: {dados_cnpj}")
            
            
            valor = dados_pagamento.get("valor", 0)
            cnpj = dados_pagamento.get("cnpj", "Desconecido")
            data = dados_pagamento.get("data", "Desconecido")
            data = datetime.strptime(data, "%Y-%m-%d").date() if data != "Desconecido" else "Desconecido"
            
            razao_social = dados_cnpj.get("razao_social", "Desconecido")
            estabelecimento = dados_cnpj.get("nome_fantasia", "Desconecido")
            estabelecimento.strip() if estabelecimento else "Desconecido"
            cnae_principal = dados_cnpj.get("cnae_principal") or {}
            categoria = cnae_principal.get("descricao", "Desconhecido") if isinstance(cnae_principal, dict) else str(cnae_principal)
            ramo = categoria
            
            
            func_id = await funcionario_service.get_funcionario_id_by_telefone(telefone)
            print(f"ID do funcionário encontrado: {func_id}")

            gastos_service.cadastrar_gasto(
                funcionario_id=func_id,
                motivo=dados_pagamento.get("categoria") or "Consumo",
                descricao=f"Comprovante enviado via WhatsApp: {file.filename}",
                valor=valor,
                cnpj=cnpj,
                data=data, # Certifique-se que já converteu para date!
                empresa=estabelecimento,
                razao_social=razao_social,
                ramo_atividade=ramo,
                categoria=categoria,
                arquivo_extracao=caminho_final,
                tipo_gasto="Dinheiro Funcionário"
            )
            print(f"Gasto cadastrado com sucesso para o funcionário ID: {func_id}")
            
            return dados_pagamento, dados_cnpj

        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            return None
    elif file.content_type == 'application/pdf':
        try:
            pasta_destino_pdf = os.path.join(pasta_destino, 'pdf')
            os.makedirs(pasta_destino_pdf, exist_ok=True)

            data_hora_atual = obter_data_hora_atual()
            nome_arquivo = f"comprovante_{telefone}_{data_hora_atual}_{file.filename}"
            caminho_completo = os.path.join(pasta_destino_pdf, nome_arquivo)

            pdf_bytes = await file.read()
            with open(caminho_completo, "wb") as buffer:
                buffer.write(pdf_bytes)

            print(f"PDF salvo com sucesso em: {caminho_completo}")
            await file.seek(0)

            dados_pagamento, dados_cnpj = await scrape_pdf(pdf_bytes)
            print(f"Dados extraídos do PDF: {dados_pagamento}")
            print(f"Dados da empresa consultados: {dados_cnpj}")
            print(type(dados_cnpj) == dict)
            valor = dados_pagamento.get("valor", 0)
            cnpj = dados_pagamento.get("cnpj", "Desconecido")
            data_str = dados_pagamento.get("data", "Desconecido")
            print(f"Data extraída do PDF (objeto datetime): {data_str}")
            if data_str != "Desconecido":
                data_obj = datetime.strptime(data_str, "%d/%m/%Y")
                print(f"Data extraída do PDF (objeto datetime): {data_obj}")
                data_sql = data_obj.strftime("%Y-%m-%d")
                print(f"Data convertida para formato SQL: {data_sql}")
            else:
                data_sql = None
            
            razao_social = dados_cnpj.get("razao_social", "Desconecido")
            estabelecimento = dados_cnpj.get("nome_fantasia", "Desconecido")
            estabelecimento.strip() if estabelecimento else "Desconecido"
            cnae_principal = dados_cnpj.get("cnae_principal") or {}
            categoria = cnae_principal.get("descricao", "Desconhecido") if isinstance(cnae_principal, dict) else str(cnae_principal)
            ramo = categoria

            func_id = await funcionario_service.get_funcionario_id_by_telefone(telefone)
            print(f"ID do funcionário encontrado: {func_id}")
            
            
            # 1. Lê o formato brasileiro
            objeto_data = datetime.strptime(data, "%d/%m/%Y")

            # 2. Transforma no formato que o SQLite/MySQL aceita
            data_sql = objeto_data.strftime("%Y-%m-%d")


            gastos_service.cadastrar_gasto(
                funcionario_id=func_id,
                motivo=dados_pagamento.get("categoria") or "Consumo",
                descricao=f"Comprovante enviado via WhatsApp: {file.filename}",
                valor=valor,
                cnpj=cnpj,
                data=data_sql, # Certifique-se que já converteu para date!
                empresa=estabelecimento,
                razao_social=razao_social,
                ramo_atividade=ramo,
                categoria=categoria,
                arquivo_extracao=caminho_final,
                tipo_gasto="Dinheiro Funcionário"
            )
            print(f"Gasto cadastrado com sucesso para o funcionário ID: {func_id}")
            
            return dados_pagamento, dados_cnpj

        except Exception as e:
            print(f"Erro ao processar PDF: {e}")
            return None
