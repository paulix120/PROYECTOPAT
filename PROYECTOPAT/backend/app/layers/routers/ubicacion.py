from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.business.ubicacion_service import UbicacionService
from app.layers.models.ubicacion import UbicacionCreate, UbicacionUpdate, UbicacionResponse

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones Geográficas"])

@router.post("/", response_model=UbicacionResponse, status_code=201)
def crear_ubicacion(data: UbicacionCreate, db: Session = Depends(get_session)):
    return UbicacionService.crear_ubicacion(db, data)

@router.get("/", response_model=List[UbicacionResponse])
def listar_ubicaciones(db: Session = Depends(get_session)):
    return UbicacionService.listar_ubicaciones(db)

@router.put("/{id_ubi}", response_model=UbicacionResponse)
def actualizar_ubicacion(id_ubi: int, data: UbicacionUpdate, db: Session = Depends(get_session)):
    return UbicacionService.actualizar_ubicacion(db, id_ubi, data)

@router.delete("/{id_ubi}")
def eliminar_ubicacion(id_ubi: int, db: Session = Depends(get_session)):
    return UbicacionService.eliminar_ubicacion(db, id_ubi)