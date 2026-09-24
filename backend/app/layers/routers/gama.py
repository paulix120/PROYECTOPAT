from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.models.gama import Gama
from app.layers.business.gama_service import GamaService

router = APIRouter(
    prefix="/gamas",
    tags=["Catálogos - Turismo"]
)

@router.get("/", response_model=List[Gama])
def obtener_todos(db: Session = Depends(get_session)):
    return GamaService.obtener_todos(db)

@router.get("/{id_gama}", response_model=Gama)
def obtener_por_id(id_gama: int, db: Session = Depends(get_session)):
    return GamaService.obtener_por_id(db, id_gama)