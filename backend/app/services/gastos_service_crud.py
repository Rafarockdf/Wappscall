from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import funcionario_repo # Use a instância global
from backend.app.repositories import gastos_repo
from datetime import datetime


class GastosService:
    def criar_gasto(self, valor, cnpj, data, estabelecimento, pagador):
        with DBConnectionHandler() as db:
            session = db.get_session()
            
            dados_gasto = {
                "valor": valor,
                "cnpj": cnpj,
                "data": data,
                "estabelecimento": estabelecimento,
                "pagador": pagador
            }
            
            return gastos_repo.inserir(session, dados_gasto)
        
    def cadastrar_gasto(self, valor, cnpj, data, estabelecimento, pagador):
        return self.criar_gasto(valor, cnpj, data, estabelecimento, pagador)