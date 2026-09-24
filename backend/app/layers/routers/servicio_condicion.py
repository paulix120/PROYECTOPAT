from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user, require_role
from app.layers.models.auth import User
from app.layers.models.servicio_condicion import ServicioCondicion, ServicioCondicionCreate
from app.layers.business.servicio_condicion_service import ServicioCondicionService

router = APIRouter(prefix="/servicio-condiciones", tags=["Fase 3 - Condiciones de Servicios"])

@router.post("/", response_model=ServicioCondicion, dependencies=[Depends(require_role(3))])
def asignar_condicion(data: ServicioCondicionCreate, db: Session = Depends(get_session), usuario_actual: User = Depends(get_current_user)):
    return ServicioCondicionService.asignar_condicion(db, data, usuario_actual)

@router.delete("/{id_servicio_condi}", dependencies=[Depends(require_role(3))])
def remover_condicion(id_servicio_condi: int, db: Session = Depends(get_session), usuario_actual: User = Depends(get_current_user)):
    return ServicioCondicionService.remover_condicion(db, id_servicio_condi, usuario_actual)