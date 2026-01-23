"""
Constantes da aplicação
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Backend
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")

# WhatsApp
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
WHATSAPP_API_VERSION = "v17.0"
WHATSAPP_API_URL = f"https://graph.instagram.com/{WHATSAPP_API_VERSION}"

# Configurações de Requisição
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))  # segundos

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# Limites
MAX_MESSAGE_LENGTH = 4096
MIN_MESSAGE_LENGTH = 1
MAX_WEBHOOK_RETRIES = 3

# Status do Bot
BOT_NAME = "Wappscal"
BOT_VERSION = "1.0.0"

# Mensagens Padrão
MSG_WELCOME = "Bem-vindo ao Wappscal! 👋"
MSG_ERROR = "❌ Desculpe, ocorreu um erro. Tente novamente."
MSG_TIMEOUT = "⏱️ Requisição expirou. Tente novamente."
MSG_NOT_FOUND = "🔍 Dado não encontrado."
MSG_UNAUTHORIZED = "🔐 Não autorizado."
MSG_FORBIDDEN = "🚫 Acesso proibido."

# Tipos de Mensagem
MESSAGE_TYPE_TEXT = "text"
MESSAGE_TYPE_IMAGE = "image"
MESSAGE_TYPE_AUDIO = "audio"
MESSAGE_TYPE_VIDEO = "video"
MESSAGE_TYPE_DOCUMENT = "document"
MESSAGE_TYPE_LOCATION = "location"
MESSAGE_TYPE_CONTACTS = "contacts"

# Emojis Personalizados
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_WARNING = "⚠️"
EMOJI_INFO = "ℹ️"
EMOJI_LOADING = "⏳"
EMOJI_CLOCK = "⏰"
EMOJI_PHONE = "📱"
EMOJI_MESSAGE = "💬"
EMOJI_USER = "👤"
EMOJI_SETTINGS = "⚙️"
EMOJI_HELP = "❓"
EMOJI_MENU = "📋"

# Cache
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # segundos

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")

# Features
FEATURE_SEARCH = os.getenv("FEATURE_SEARCH", "True").lower() == "true"
FEATURE_HISTORY = os.getenv("FEATURE_HISTORY", "True").lower() == "true"
FEATURE_NOTIFICATIONS = os.getenv("FEATURE_NOTIFICATIONS", "True").lower() == "true"
