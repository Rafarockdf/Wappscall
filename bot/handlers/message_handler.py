"""
Handler para processar mensagens de texto comuns
"""
#from typing import Optional
#from bot.utils.logger import get_logger
#from bot.utils.http_client import HTTPClient
#from bot.utils.formatters import format_response
#from bot.utils.validators import validate_user_input
from bot.utils.helpers import extract_user_data
#logger = get_logger(__name__)
from bot.utils.http_client import BackendClient



async def register_handlers(bot):
    @bot.message_handler(content_types=['text'])
    async def send_welcome(message):
        user_info = await extract_user_data(message)

        resposta = (
            "Olá! Eu sou um bot <b>Wappscall</b> gerenciador de gastos 🤖.\n\n"
            "<b>Digite 1 para enviar comprovante por imagem ou pdf.</b>\n"
            
        )

        print(f"Usuário {user_info['username']} iniciou o bot.")
        await bot.reply_to(message, 
            resposta, parse_mode='HTML'
        )

    @bot.message_handler(content_types=['photo', 'document'])
    async def handle_docs(message):
        # 1. Pega o ID do arquivo (seja foto ou documento)
        api_client = BackendClient(base_url="http://127.0.0.1:8000")

        file_id = message.photo[-1].file_id if message.photo else message.document.file_id
        file_name = f"comprovante_{message.from_user.id}.jpg"
        
        # 2. Baixa o arquivo do Telegram para a memória (bytes)
        file_info = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        
        # 3. A LINHA QUE VOCÊ QUERIA: Envia para a API
        try:
            print("Enviando para o backend...")
            result = await api_client.upload_comprovante(downloaded_file, file_name)
            await bot.reply_to(message, f"✅ Recebido! Arquivo salvo em: <code>{result['path']}</code>", parse_mode='HTML')
        except Exception as e:
            await bot.reply_to(message, f"❌ Erro ao salvar no servidor: {e}")
