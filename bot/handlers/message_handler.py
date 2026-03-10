from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot.utils.http_client import BackendClient

def register_handlers(bot):
    
    # TESTE DE EMERGÊNCIA PARA O START
    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        await bot.reply_to(message, "Olá! O bot está vivo. Envie o seu PDF agora.")
    
    @bot.message_handler(content_types=['photo', 'document'])
    async def handle_docs(message):
        api_client = BackendClient(base_url="http://localhost:8000")

        # Ponto 2 da Task: Conseguir as infos e o nome do arquivo
        if message.photo:
            file_id = message.photo[-1].file_id
            file_name = f"foto_{message.from_user.id}.jpg"
            content_type = 'image/jpeg'
        else:
            file_id = message.document.file_id
            file_name = message.document.file_name # Mantém o nome original!
            content_type = message.document.mime_type

        # Ponto 3 da Task: Enviar e Gravar Arquivo
        file_info = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        
        try:
            # Envia para o backend (que vai gravar na pasta uploads)
            await api_client.upload_comprovante(downloaded_file, file_name, content_type)
            await bot.reply_to(message, f"✅ Arquivo {file_name} enviado e armazenado!")
            
            # Ponto 3: Coletar número do usuário
            await solicitar_telefone(message, bot)
            
        except Exception as e:
            await bot.reply_to(message, f"❌ Erro ao enviar: {e}")

    async def solicitar_telefone(message, bot):
        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = KeyboardButton(text="Enviar Telefone", request_contact=True)
        markup.add(button_phone)
        await bot.send_message(message.chat.id, "Por favor, compartilhe seu contato:", reply_markup=markup)

    # Handler para receber o contato
    @bot.message_handler(content_types=['contact'])
    async def handle_contact(message):
        print(f"Telefone recebido: {message.contact.phone_number}")
        await bot.reply_to(message, "Obrigado! Contato recebido.")