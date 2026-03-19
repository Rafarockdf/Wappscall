import os
import sys
caminho_absoluto = os.path.abspath(os.curdir)
sys.path.insert(0, caminho_absoluto)
from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import funcionario_repo
from backend.app.repositories.repositories import gastos_repo
def listar_funcionarios():
    with DBConnectionHandler() as db:
        session = db.get_session()
        return funcionario_repo.buscar_todos(session)

def listar_gastos():
    with DBConnectionHandler() as db:
        session = db.get_session()
        return gastos_repo.buscar_todos(session)



if __name__ == "__main__":
    for f in listar_funcionarios():
        print(f.id, f.nome, f.cargo, f.salario, f.telefone, f.data_contratacao)
    for g in listar_gastos():
        print(f"ID: {g.id} | Motivo: {g.motivo} | Valor: R${g.valor:.2f} | Data: {g.data} | "
                  f"Empresa: {g.empresa} | CNPJ: {g.cnpj} | Razão Social: {g.razao_social} | "
                  f"Ramo: {g.ramo_atividade} | Categoria: {g.categoria} | Tipo: {g.tipo_gasto} | "
                  f"Arquivo: {g.arquivo_extracao} | Aprovado: {g.boolean_aprovado} | "
                  f"Extornado: {g.boolean_extornado} | Func_ID: {g.funcionario_id} | User_ID: {g.usuario_id}")