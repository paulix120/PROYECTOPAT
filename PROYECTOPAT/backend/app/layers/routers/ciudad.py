from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.business.ciudad_service import CiudadService
from app.layers.models.ciudad import CiudadResponse

router = APIRouter(prefix="/ciudades", tags=["Geografía Nivel 3 - Ciudades"])

@router.get("/", response_model=List[CiudadResponse])
def obtener_ciudades(db: Session = Depends(get_session)):
    return CiudadService.listar_ciudades(db)

@router.get("/{id_cdad}", response_model=CiudadResponse)
def obtener_ciudad_por_id(id_cdad: int, db: Session = Depends(get_session)):
    return CiudadService.obtener_ciudad(db, id_cdad)

@router.get("/departamento/{id_depart}", response_model=List[CiudadResponse])
def obtener_ciudades_por_departamento(id_depart: int, db: Session = Depends(get_session)):
    return CiudadService.listar_por_departamento(db, id_depart)