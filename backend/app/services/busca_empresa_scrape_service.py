import os
import sys
from dotenv import load_dotenv
import httpx # Trocando requests por httpx

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
load_dotenv()

usuario = os.getenv("EMAIL_USER")
URL_API_BUSCA_CNPJ = os.getenv("URL_API_BUSCA_CNPJ")

async def consultar_cnpj(cnpj):
    # 1. Blindagem contra variáveis nulas do .env
    if not URL_API_BUSCA_CNPJ:
        print("Erro: A variável URL_API_BUSCA_CNPJ não foi encontrada no .env")
        return None

    # Substitui a tag {cnpj} pelo cnpj real
    url = URL_API_BUSCA_CNPJ.replace("CNPJ", str(cnpj))

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 2. Uso do httpx assíncrono para não travar o servidor
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
        except httpx.RequestError as exc:
            print(f"Erro de conexão com a API: {exc}")
            return None

    if response.status_code != 200:
        print(f"Erro ao consultar API. Status code: {response.status_code}")
        return None

    dados = response.json()

    if dados.get("status") == "ERROR":
        print("Erro:", dados.get("message"))
        return None

    resultado = {
        "cnpj": dados.get("cnpj"),
        "razao_social": dados.get("razao_social"),
        "nome_fantasia": dados.get("nome_fantasia"),
        "situacao_cadastral": dados.get("situacao_cadastral"),
        "data_situacao_cadastral": dados.get("data_situacao_cadastral"),
        "matriz_filial": dados.get("matriz_filial"),
        "data_inicio_atividade": dados.get("data_inicio_atividade"),
        "cnae_principal": dados.get("cnae_principal"),
        "cnaes_secundarios": dados.get("cnaes_secundarios", []),
        "cnaes_secundarios_count": dados.get("cnaes_secundarios_count"),
        "natureza_juridica": dados.get("natureza_juridica"),
        "logradouro": dados.get("logradouro"),
        "numero": dados.get("numero"),
        "complemento": dados.get("complemento"),
        "bairro": dados.get("bairro"),
        "cep": dados.get("cep"),
        "uf": dados.get("uf"),
        "municipio": dados.get("municipio"),
        "email": dados.get("email"),
        
        # Como telefones agora é uma lista de dicionários, podemos formatar para uma string única 
        # (Ex: "11900000000") ou pegar a lista inteira. Aqui estou extraindo apenas os números juntos:
        "telefones": [f"{tel.get('ddd', '')}{tel.get('numero', '')}" for tel in dados.get("telefones", [])],
        
        "capital_social": dados.get("capital_social"),
        "porte_empresa": dados.get("porte_empresa"),
        "opcao_simples": dados.get("opcao_simples"),
        "data_opcao_simples": dados.get("data_opcao_simples"),
        "opcao_mei": dados.get("opcao_mei"),
        "data_opcao_mei": dados.get("data_opcao_mei"),
        
        # Mapeando os nomes dos sócios conforme a nova chave "nome_socio" dentro da lista "QSA"
        "socios": [socio.get("nome_socio") for socio in dados.get("QSA", [])]
    }

    return resultado