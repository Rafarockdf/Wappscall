from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import gastos_repo
from datetime import datetime


def get_gastos() -> list[dict]:
    with DBConnectionHandler() as db:
        session = db.get_session()
        gastos = gastos_repo.buscar_todos(session)
        result = []
        for g in gastos:
            result.append({
                "id": g.id,
                "motivo": g.motivo,
                "descricao": g.descricao,
                "valor": g.valor,
                "data": str(g.data) if g.data else None,
                "empresa": g.empresa,
                "cnpj": g.cnpj,
                "razao_social": g.razao_social,
                "ramo_atividade": g.ramo_atividade,
                "categoria": g.categoria,
                "tipo_gasto": g.tipo_gasto,
                "boolean_aprovado": g.boolean_aprovado,
                "data_aprovacao": str(g.data_aprovacao) if g.data_aprovacao else None,
                "boolean_extornado": g.boolean_extornado,
                "data_extorno": str(g.data_extorno) if g.data_extorno else None,
                "arquivo_extracao": g.arquivo_extracao,
                "funcionario_id": g.funcionario_id,
                "funcionario_nome": g.funcionario.nome if g.funcionario else None,
            })
        return result


def atualizar_status_gasto(gasto_id: int, status: dict) -> bool:
    with DBConnectionHandler() as db:
        session = db.get_session()

        gasto = gastos_repo.buscar_por_id(session, gasto_id)
        if not gasto:
            return False

        gasto.boolean_aprovado = status["aprovado"]
        gasto.boolean_extornado = status["extornado"]

        if status["aprovado"]:
            gasto.data_aprovacao = datetime.now().date()
        else:
            gasto.data_aprovacao = None

        if status["extornado"]:
            gasto.data_extorno = datetime.now().date()
        else:
            gasto.data_extorno = None

        session.commit()
        return True