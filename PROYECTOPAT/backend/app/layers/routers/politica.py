from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.business.politica_service import PoliticaService
from app.layers.models.politica import PoliticaCreate, PoliticaUpdate, PoliticaResponse

router = APIRouter(prefix="/politicas", tags=["Módulo - Políticas y Condiciones"])

@router.post("/", response_model=PoliticaResponse, status_code=201)
def crear_politica(data: PoliticaCreate, db: Session = Depends(get_session)):
    return PoliticaService.crear_politica(db, data)

@router.get("/", response_model=List[PoliticaResponse])
def listar_politicas(db: Session = Depends(get_session)):
    return PoliticaService.listar_politicas(db)

@router.put("/{id_poli}", response_model=PoliticaResponse)
def actualizar_politica(id_poli: int, data: PoliticaUpdate, db: Session = Depends(get_session)):
    return PoliticaService.actualizar_politica(db, id_poli, data)

@router.delete("/{id_poli}")
def eliminar_politica(id_poli: int, db: Session = Depends(get_session)):
    return PoliticaService.eliminar_politica(db, id_poli)