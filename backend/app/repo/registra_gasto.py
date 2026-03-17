import os
import sys

caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)

from backend.database.config.connection import DBConnectionHandler
from backend.app.repo.repositories import gasto_repo

class RegistraGasto:
    def __init__(self, valor, cnpj, data, estabelecimento, pagador):
        self.valor = valor
        self.cnpj = cnpj
        self.data = data
        self.estabelecimento = estabelecimento
        self.pagador = pagador

    def registrar_gasto(self):
        with DBConnectionHandler() as db:
            session = db.get_session()
            
            dados_gasto = {
                "valor": self.valor,
                "cnpj": self.cnpj,
                "data": self.data,
                "estabelecimento": self.estabelecimento,
                "pagador": self.pagador
            }
            
            novo_gasto = gasto_repo.inserir(session, dados_gasto)
            return novo_gasto