from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.business.condicion_service import CondicionService
from app.layers.models.condicion import CondicionCreate, CondicionUpdate, CondicionResponse

router = APIRouter(prefix="/condiciones", tags=["Módulo - Políticas y Condiciones"])

@router.post("/", response_model=CondicionResponse, status_code=201)
def crear_condicion(data: CondicionCreate, db: Session = Depends(get_session)):
    return CondicionService.crear_condicion(db, data)

@router.get("/", response_model=List[CondicionResponse])
def listar_condiciones(db: Session = Depends(get_session)):
    return CondicionService.listar_condiciones(db)

@router.put("/{id_condi}", response_model=CondicionResponse)
def actualizar_condicion(id_condi: int, data: CondicionUpdate, db: Session = Depends(get_session)):
    return CondicionService.actualizar_condicion(db, id_condi, data)

@router.delete("/{id_condi}")
def eliminar_condicion(id_condi: int, db: Session = Depends(get_session)):
    return CondicionService.eliminar_condicion(db, id_condi)