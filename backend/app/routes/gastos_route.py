from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    funcionario_nome: Optional[str] = None


class AtualizarStatusRequest(BaseModel):
    status: str


@router.get("/gastos", response_model=list[GastoResponse])
def listar_gastos():
    from backend.app.services.gastos_service import get_gastos
    return get_gastos()


@router.put("/gastos/{gasto_id}/status")
def atualizar_status_gasto(gasto_id: int, request: AtualizarStatusRequest):
    from backend.app.services.gastos_service import atualizar_status_gasto

    status_map = {
        "Pendente": {"aprovado": False, "extornado": False},
        "Aprovado": {"aprovado": True, "extornado": False},
        "Extornado": {"aprovado": False, "extornado": True}
    }

    if request.status not in status_map:
        raise HTTPException(status_code=400, detail="Status inválido")

    success = atualizar_status_gasto(gasto_id, status_map[request.status])

    if not success:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")

    return {"message": "Status atualizado com sucesso"}