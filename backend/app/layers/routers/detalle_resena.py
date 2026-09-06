from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.layers.business.detalle_resena_service import DetalleResenaService
from app.layers.models.detalle_resena import (
    DetalleResenaCreate,
    DetalleResenaResponse,
    DetalleResenaUpdate,
)

router = APIRouter(prefix="/detalles-resena", tags=["Módulo - Reseñas"])

@router.post("", response_model=DetalleResenaResponse, status_code=status.HTTP_201_CREATED)
def crear_detalle(data: DetalleResenaCreate, db: Session = Depends(get_session)):
    return DetalleResenaService.crear_detalle(db, data)

@router.get("/resena/{id_resena}", response_model=List[DetalleResenaResponse])
def listar_por_resena(id_resena: int, db: Session = Depends(get_session)):
    return DetalleResenaService.listar_por_resena(db, id_resena)

@router.get("/{id_detalle}", response_model=DetalleResenaResponse)
def obtener_detalle(id_detalle: int, db: Session = Depends(get_session)):
    return DetalleResenaService.obtener_por_id(db, id_detalle)

@router.put("/{id_detalle}", response_model=DetalleResenaResponse)
def actualizar_detalle(id_detalle: int, data: DetalleResenaUpdate, db: Session = Depends(get_session)):
    return DetalleResenaService.actualizar_detalle(db, id_detalle, data)

@router.delete("/{id_detalle}")
def eliminar_detalle(id_detalle: int, db: Session = Depends(get_session)):
    return DetalleResenaService.eliminar_detalle(db, id_detalle)