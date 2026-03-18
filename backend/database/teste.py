import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import funcionario_repo

def listar_funcionarios():
    with DBConnectionHandler() as db:
        session = db.get_session()
        return funcionario_repo.buscar_todos(session)

if __name__ == "__main__":
    for f in listar_funcionarios():
        print(f.id, f.nome, f.cargo, f.salario, f.telefone, f.data_contratacao)