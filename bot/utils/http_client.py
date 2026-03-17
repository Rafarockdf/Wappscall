import aiohttp

class BackendClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def upload_comprovante(self, file_bytes: bytes, file_name: str, content_type: str, telefone: str):
        # Rota correta conforme o seu backend/app/main.py
        url = f"{self.base_url.rstrip('/')}/uploads/uploads"
        
        data = aiohttp.FormData()
        # Aqui enviamos o arquivo com o NOME ORIGINAL e o TIPO correto
        data.add_field('file', 
                       file_bytes, 
                       filename=file_name, 
                       content_type=content_type)
        # Adiciona o telefone como um campo separado
        data.add_field('telefone', telefone)
        

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    text = await response.text()
                    raise Exception(f"Erro na API: {response.status} - {text}")