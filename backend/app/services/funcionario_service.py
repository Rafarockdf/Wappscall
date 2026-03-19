from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import funcionario_repo # Use a instância global
from datetime import datetime

class FuncionarioService:
    async def criar_funcionario(self, nome, cargo, salario, data_contratacao, telefone):
        with DBConnectionHandler() as db:
            session = db.get_session()
            
            # CORREÇÃO: Crie um DICIONÁRIO com os dados
            dados_funcionario = {
                "nome": nome,
                "cargo": cargo,
                "salario": salario,
                "data_contratacao": data_contratacao,
                "telefone": telefone
            }
            
            # O BaseRepo vai receber o dicionário e fazer o trabalho de criar o objeto
            return funcionario_repo.inserir(session, dados_funcionario)
        
    async def cadastrar_funcionario(self, nome, cargo, salario, data_contratacao, telefone):
        return await self.criar_funcionario(nome, cargo, salario, data_contratacao, telefone)
    async def get_funcionario_id_by_telefone(self, telefone):
        with DBConnectionHandler() as db:
            session = db.get_session()
            funcionario = funcionario_repo.buscar_por_telefone(session, telefone)
            return funcionario.id if funcionario else None