from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.models.tp_servicio import TpServicio
from app.layers.business.tp_servicio_service import TpServicioService

router = APIRouter(
    prefix="/tipos-servicio",
    tags=["Catálogos - Turismo"]
)

@router.get("/", response_model=List[TpServicio])
def obtener_todos(db: Session = Depends(get_session)):
    return TpServicioService.obtener_todos(db)

@router.get("/{id_tp_serv}", response_model=TpServicio)
def obtener_por_id(id_tp_serv: int, db: Session = Depends(get_session)):
    return TpServicioService.obtener_por_id(db, id_tp_serv)