import os
import sys
from PIL import Image
from fastapi import UploadFile
from dotenv import load_dotenv
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
load_dotenv()
async def save_image_file(file: UploadFile):
    # 1. Puxar o caminho da variável de ambiente (com um fallback para 'uploads')
    pasta_destino = os.getenv('CAMINHO_IMAGENS', 'uploads')

    # 2. Criar a pasta se ela não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    try:
        # 3. Ler o conteúdo do UploadFile
        # Usamos io.BytesIO para que a PIL possa ler os bytes vindos da memória
        conteudo = await file.read()
        img = Image.open(io.BytesIO(conteudo))

        # 4. Definir o caminho final
        # Usamos o nome original do arquivo ou um nome padrão
        nome_arquivo = f"copy_{file.filename}"
        caminho_final = os.path.join(pasta_destino, nome_arquivo)

        # 5. Salvar a imagem
        # Se quiser manter o formato original, pode usar img.format
        img.save(caminho_final)

        print(f"Imagem salva com sucesso em: {caminho_final}")
        return caminho_final

    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None
