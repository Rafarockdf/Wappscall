import os
import sys

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

from backend.database.config.connection import DBConnectionHandler
from backend.database.config.base import Base

class RegistraGasto:
    def __init__(self, valor, categoria, data, descricao):
        self.valor = valor
        self.categoria = categoria
        self.data = data
        self.descricao = descricao

    def registrar_gasto(self):
        with DBConnectionHandler() as db_handler:
            session = db_handler.get_session()
            # Aqui você pode criar um objeto de gasto e adicioná-lo à sessão
            # Exemplo:
            # novo_gasto = Gasto(valor=self.valor, categoria=self.categoria, data=self.data, descricao=self.descricao)
            # session.add(novo_gasto)
            session.commit()