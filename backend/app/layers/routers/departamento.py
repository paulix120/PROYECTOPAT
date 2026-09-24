from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.business.departamento_service import DepartamentoService
from app.layers.models.departamento import DepartamentoResponse

router = APIRouter(prefix="/departamentos", tags=["Geografía Nivel 2 - Departamentos"])

@router.get("/", response_model=List[DepartamentoResponse])
def obtener_departamentos(db: Session = Depends(get_session)):
    return DepartamentoService.listar_departamentos(db)

@router.get("/{id_depart}", response_model=DepartamentoResponse)
def obtener_departamento_por_id(id_depart: int, db: Session = Depends(get_session)):
    return DepartamentoService.obtener_departamento(db, id_depart)

@router.get("/pais/{id_pais}", response_model=List[DepartamentoResponse])
def obtener_departamentos_por_pais(id_pais: int, db: Session = Depends(get_session)):
    return DepartamentoService.listar_por_pais(db, id_pais)