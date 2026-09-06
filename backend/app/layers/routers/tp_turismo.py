from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.models.tp_turismo import TpTurismo
from app.layers.business.tp_turismo_service import TpTurismoService

router = APIRouter(
    prefix="/tipos-turismo",
    tags=["Catálogos - Turismo"]
)

@router.get("/", response_model=List[TpTurismo])
def obtener_todos(db: Session = Depends(get_session)):
    return TpTurismoService.obtener_todos(db)

@router.get("/{id_tp_turi}", response_model=TpTurismo)
def obtener_por_id(id_tp_turi: int, db: Session = Depends(get_session)):
    return TpTurismoService.obtener_por_id(db, id_tp_turi)