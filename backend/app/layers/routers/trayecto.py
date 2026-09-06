from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.business.trayecto_service import TrayectoService
from app.layers.models.trayecto import TrayectoCreate, TrayectoUpdate, TrayectoResponse

router = APIRouter(prefix="/trayectos", tags=["Trayectos y Rutas"])

@router.post("/", response_model=TrayectoResponse, status_code=201)
def crear_trayecto(data: TrayectoCreate, db: Session = Depends(get_session)):
    return TrayectoService.crear_trayecto(db, data)

@router.get("/", response_model=List[TrayectoResponse])
def listar_trayectos(db: Session = Depends(get_session)):
    return TrayectoService.listar_trayectos(db)

@router.put("/{id_tray}", response_model=TrayectoResponse)
def actualizar_trayecto(id_tray: int, data: TrayectoUpdate, db: Session = Depends(get_session)):
    return TrayectoService.actualizar_trayecto(db, id_tray, data)

@router.delete("/{id_tray}")
def eliminar_trayecto(id_tray: int, db: Session = Depends(get_session)):
    return TrayectoService.eliminar_trayecto(db, id_tray)