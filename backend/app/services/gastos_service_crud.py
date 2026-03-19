from backend.database.config.connection import DBConnectionHandler
from backend.app.repositories.repositories import funcionario_repo # Use a instância global
from backend.app.repositories.repositories import gastos_repo
from datetime import datetime


class GastosService:
    def criar_gasto(
            self, 
            funcionario_id: int, 
            motivo: str, 
            descricao: str, 
            valor: float, 
            cnpj: str, 
            data: datetime, 
            empresa: str, 
            razao_social: str, 
            ramo_atividade: str, 
            categoria: str, 
            arquivo_extracao: str = None, 
            tipo_gasto: str = "Dinheiro Funcionário",
            usuario_id: int = None
        ):
            with DBConnectionHandler() as db:
                session = db.get_session()
                
                dados_gasto = {
                    "funcionario_id": funcionario_id,
                    "usuario_id": usuario_id,
                    "motivo": motivo,
                    "descricao": descricao,
                    "valor": valor,
                    "cnpj": cnpj,
                    "data": data,
                    "empresa": empresa,
                    "razao_social": razao_social,
                    "ramo_atividade": ramo_atividade,
                    "categoria": categoria,
                    "arquivo_extracao": arquivo_extracao,
                    "tipo_gasto": tipo_gasto
                }
                
                # O gastos_repo usará o BaseRepo para fazer o insert
                return gastos_repo.inserir(session, dados_gasto)

    def cadastrar_gasto(self, **kwargs):
            return self.criar_gasto(**kwargs)