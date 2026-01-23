"""
Utilidades e funções auxiliares do bot
"""
import os
import sys

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
#from bot.utils.logger import get_logger
#from bot.utils.validators import validate_user_input, validate_phone
#from bot.utils.formatters import format_response, format_error
#from bot.utils.http_client import HTTPClient
#from bot.utils.constants import *

__all__ = [
    "get_logger",
    "validate_user_input",
    "validate_phone",
    "format_response",
    "format_error",
    "HTTPClient",
]
