from typing import List # Agrega esto
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user, require_role
from app.layers.models.auth import User
from app.layers.models.servicio import Servicio, HospedajeBaseCreate, HospedajeEspacioCreate, HospedajeBaseUpdate, HospedajeEspacioUpdate # Agrega 'Servicio' aquí
from app.layers.business.servicio_service import ServicioService

router = APIRouter(prefix="/servicios", tags=["Oferta Turística (Fase 3)"])

# ================= GET =================

# -----> ESTE ES EL NUEVO ENDPOINT GENERAL <-----
from typing import Any
@router.get("/", response_model=List[Any])
def listar_todos_los_servicios(db: Session = Depends(get_session)):
    """
    Retorna TODOS los servicios registrados en la plataforma (Hospedaje, Gastronomía, Recreación, etc).
    """
    return ServicioService.listar_todos_los_servicios(db)

@router.get("/hospedajes")
def listar_hospedajes(db: Session = Depends(get_session)):
    return ServicioService.listar_alojamientos_con_espacios(db)

# ================= POST =================
@router.post("/hospedajes/base", dependencies=[Depends(require_role(3))])
def crear_alojamiento_base(data: HospedajeBaseCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioService.crear_hotel_base(db, data, usuario)

@router.post("/hospedajes/{id_servicio}/espacios", dependencies=[Depends(require_role(3))])
def agregar_habitacion(id_servicio: int, data: HospedajeEspacioCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioService.agregar_espacio_hospedaje(db, id_servicio, data, usuario)

# ================= PUT =================
@router.put("/hospedajes/base/{id_servicio}", dependencies=[Depends(require_role(3))])
def editar_alojamiento_base(id_servicio: int, data: HospedajeBaseUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioService.actualizar_hotel_base(db, id_servicio, data, usuario)

@router.put("/hospedajes/espacios/{id_hosp}", dependencies=[Depends(require_role(3))])
def editar_habitacion(id_hosp: int, data: HospedajeEspacioUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioService.actualizar_espacio(db, id_hosp, data, usuario)

# ================= DELETE =================
@router.delete("/hospedajes/base/{id_servicio}", dependencies=[Depends(require_role(3))])
def borrar_alojamiento(id_servicio: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioService.eliminar_hotel_base(db, id_servicio, usuario)

@router.delete("/hospedajes/espacios/{id_hosp}", dependencies=[Depends(require_role(3))])
def borrar_habitacion(id_hosp: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioService.eliminar_espacio(db, id_hosp, usuario)