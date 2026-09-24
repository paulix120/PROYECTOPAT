from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user, require_role
from app.layers.models.auth import User
from app.layers.models.servicio_guia import GuiaCreate, GuiaUpdate
from app.layers.business.servicio_guia_service import ServicioGuiaService

router = APIRouter(prefix="/servicios/guias", tags=["Oferta Turística - Guías"])

@router.post("/", dependencies=[Depends(require_role(3))])
def crear(data: GuiaCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGuiaService.crear(db, data, usuario)

@router.get("/")
def listar(db: Session = Depends(get_session)):
    return ServicioGuiaService.listar(db)

@router.put("/{id_servicio}", dependencies=[Depends(require_role(3))])
def actualizar(id_servicio: int, data: GuiaUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGuiaService.actualizar(db, id_servicio, data, usuario)

@router.delete("/{id_servicio}", dependencies=[Depends(require_role(3))])
def eliminar(id_servicio: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGuiaService.eliminar(db, id_servicio, usuario)