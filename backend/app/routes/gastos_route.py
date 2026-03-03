from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class GastoResponse(BaseModel):
    id: int
    motivo: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None
    data: Optional[str] = None
    empresa: Optional[str] = None
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    ramo_atividade: Optional[str] = None
    categoria: Optional[str] = None
    tipo_gasto: Optional[str] = None
    boolean_aprovado: Optional[bool] = None
    data_aprovacao: Optional[str] = None
    boolean_extornado: Optional[bool] = None
    data_extorno: Optional[str] = None
    arquivo_extracao: Optional[str] = None
    funcionario_id: Optional[int] = None


@router.get("/gastos", response_model=list[GastoResponse])
def listar_gastos():
    from backend.app.services.gastos_service import get_gastos_mock
    return get_gastos_mock()
