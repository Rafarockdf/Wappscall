from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import funcionario_repo # Use a instância global
from datetime import datetime

class FuncionarioService:
    def criar_funcionario(self, nome, cargo, salario, data_contratacao, telefone):
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
        
    def cadastrar_funcionario(self, nome, cargo, salario, data_contratacao, telefone):
        return self.criar_funcionario(nome, cargo, salario, data_contratacao, telefone)