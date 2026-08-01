from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.layers.models.transporte import (
    MedioTransporte,
    MedioTransporteCreate,
    MedioTransporteResponse
)

router = APIRouter(prefix="/transporte", tags=["Medios de Transporte"])

@router.get("/", response_model=List[MedioTransporteResponse])
def listar_medios_transporte(db: Session = Depends(get_session)):
    """Lista todos los medios de transporte activos disponibles para planear viajes."""
    return db.exec(select(MedioTransporte).where(MedioTransporte.activo == True)).all()

@router.post("/", response_model=MedioTransporteResponse, status_code=status.HTTP_201_CREATED)
def crear_medio_transporte(
    data: MedioTransporteCreate,
    db: Session = Depends(get_session)
):
    """Permite al administrador registrar un nuevo medio de transporte y su tarifa por km."""
    nuevo_transporte = MedioTransporte.from_orm(data)
    db.add(nuevo_transporte)
    db.commit()
    db.refresh(nuevo_transporte)
    return nuevo_transporte