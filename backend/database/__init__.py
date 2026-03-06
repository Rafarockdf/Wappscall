from sqlalchemy.ext.declarative import declarative_base
import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.database.config.connection import DBConnectionHandler
from backend.database.config.base import Base

db_handler = DBConnectionHandler()
db_handler.create_tables(Base)
