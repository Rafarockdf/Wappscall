import aiohttp
import io

class BackendClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def upload_comprovante(self, file_bytes: bytes, file_name: str):
        url = f"{self.base_url}/uploads"
        
        # Prepara o formulário para envio do arquivo
        data = aiohttp.FormData()
        data.add_field('file', 
                       file_bytes, 
                       filename=file_name, 
                       content_type='application/octet-stream')

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    text = await response.text()
                    raise Exception(f"Erro na API: {response.status} - {text}")