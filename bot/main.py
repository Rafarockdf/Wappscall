import telebot
import asyncio
from telebot.async_telebot import AsyncTeleBot
import os
import sys

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

from bot.handlers.message_handler import register_handlers
from dotenv import load_dotenv


load_dotenv()

TOKEN_BOT_TELEGRAM = os.getenv("TOKEN_BOT_TELEGRAM")

async def main():
    # 1. Instancia o bot
    bot = AsyncTeleBot(TOKEN_BOT_TELEGRAM)

    # 2. Registra os handlers (comandos)
    await register_handlers(bot)

    # 3. Inicia o monitoramento de mensagens
    print("Bot rodando...")
    await bot.infinity_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot desligado manualmente.")