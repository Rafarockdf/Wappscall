import os
import sys
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils.http_client import BackendClient

def register_handlers(bot):
    
    # TESTE DE EMERGÊNCIA PARA O START
    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        await bot.reply_to(message, "Olá! O bot está vivo. Envie o seu PDF agora.")
        
    @bot.message_handler(commands=['teste'])
    async def send_welcome(message):
        await bot.reply_to(message, "Olá! leonardo maciel, como é ser gay")
    
    @bot.message_handler(content_types=['photo', 'document'])
    async def handle_docs(message):
        api_client = BackendClient(base_url="http://localhost:8000")
        nome = message.from_user.first_name
        sobrenome = message.from_user.last_name
        username = message.from_user.username
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
            telefone = await solicitar_telefone(message, bot)
            print(f"DEBUG: Telefone recebido do usuário: {telefone}")
            await api_client.upload_comprovante(downloaded_file, file_name, content_type, telefone)
            await bot.reply_to(message, f"✅ Arquivo {file_name} enviado e armazenado!")
            
            # Ponto 3: Coletar número do usuário
            
            
        except Exception as e:
            await bot.reply_to(message, f"❌ Erro ao enviar: {e}")

    esperando_telefone = {}

    async def solicitar_telefone(message, bot):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_phone = KeyboardButton(text="Compartilhar Meu Número", request_contact=True)
        markup.add(button_phone)
        
        await bot.send_message(message.chat.id, "Preciso do seu número para continuar:", reply_markup=markup)
        
        # Cria uma "promessa" (Future) para travar esta função até o usuário responder
        loop = asyncio.get_running_loop()
        futuro = loop.create_future()
        esperando_telefone[message.chat.id] = futuro
        
        # O código vai ficar pausado nesta linha até o handler de contato devolver o telefone!
        telefone = await futuro 
        return telefone

    # Handler para receber o contato
    @bot.message_handler(content_types=['contact'])
    async def handle_contact(message):
        chat_id = message.chat.id
        
        # Verifica se esse usuário estava sendo aguardado pela função solicitar_telefone
        if chat_id in esperando_telefone:
            telefone = message.contact.phone_number
            nome_contato = message.contact.first_name
            
            # Remove o botão do teclado do usuário
            remover_teclado = ReplyKeyboardRemove()
            await bot.reply_to(message, f"Obrigado, {nome_contato}! Seu número {telefone} foi salvo.", reply_markup=remover_teclado)
            
            # Envia o telefone de volta para a função 'solicitar_telefone' que estava pausada!
            esperando_telefone[chat_id].set_result(telefone)
            
            # Limpa a memória
            del esperando_telefone[chat_id]