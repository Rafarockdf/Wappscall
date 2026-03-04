import asyncio
import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from bot.handlers.message_handler import register_handlers

# Carrega as variáveis do arquivo .env
load_dotenv()
TOKEN = os.getenv("TOKEN_BOT_TELEGRAM")
print(f"DEBUG: O token que o bot está usando termina em: {TOKEN[-5:]}")

# Cria a instância do bot globalmente
bot = AsyncTeleBot(TOKEN)

async def main():
    print("Bot rodando...")
    # Registra os comandos e handlers
    register_handlers(bot) 
    # Inicia a escuta de mensagens
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())