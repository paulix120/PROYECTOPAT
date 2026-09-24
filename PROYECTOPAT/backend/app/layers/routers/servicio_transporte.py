from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user, require_role
from app.layers.models.auth import User
from app.layers.models.servicio_transporte import TransporteCreate, TransporteUpdate
from app.layers.business.servicio_transporte_service import ServicioTransporteService

router = APIRouter(prefix="/servicios/transporte", tags=["Oferta Turística - Transporte"])

@router.post("/", dependencies=[Depends(require_role(3))])
def crear(data: TransporteCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioTransporteService.crear(db, data, usuario)

@router.get("/")
def listar(db: Session = Depends(get_session)):
    return ServicioTransporteService.listar(db)

@router.put("/{id_servicio}", dependencies=[Depends(require_role(3))])
def actualizar(id_servicio: int, data: TransporteUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioTransporteService.actualizar(db, id_servicio, data, usuario)

@router.delete("/{id_servicio}", dependencies=[Depends(require_role(3))])
def eliminar(id_servicio: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioTransporteService.eliminar(db, id_servicio, usuario)