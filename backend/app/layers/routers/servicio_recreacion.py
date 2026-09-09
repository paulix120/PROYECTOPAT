from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user
from app.layers.models.auth import User
from app.layers.models.servicio_recreacion import RecreacionCreate, RecreacionUpdate
from app.layers.business.servicio_recreacion_service import ServicioRecreacionService

router = APIRouter(prefix="/servicios/recreacion", tags=["Oferta Turística - Recreación"])

@router.post("/")
def crear(data: RecreacionCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioRecreacionService.crear(db, data, usuario)

@router.get("/")
def listar(db: Session = Depends(get_session)):
    return ServicioRecreacionService.listar(db)

@router.put("/{id_servicio}")
def actualizar(id_servicio: int, data: RecreacionUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioRecreacionService.actualizar(db, id_servicio, data, usuario)

@router.delete("/{id_servicio}")
def eliminar(id_servicio: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioRecreacionService.eliminar(db, id_servicio, usuario)