from backend.database.models.models import Funcionario
from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import FuncionarioRepo



class FuncionarioService:
    def __init__(self):
        self.funcionario_repo = FuncionarioRepo()

    def criar_funcionario(self, nome, cargo, salario, data_contratacao,telefone):
        with DBConnectionHandler() as db:
            session = db.get_session()
            novo_funcionario = Funcionario(
                nome=nome,
                cargo=cargo,
                salario=salario,
                data_contratacao=data_contratacao,
                telefone=telefone
            )
            return self.funcionario_repo.inserir(session, novo_funcionario)
        
    def cadastrar_funcionario(self, nome, cargo, salario, data_contratacao,telefone):
        return self.criar_funcionario(nome, cargo, salario, data_contratacao,telefone)
    
    
    