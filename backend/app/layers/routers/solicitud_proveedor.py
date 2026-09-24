from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user, require_role
from app.layers.models.auth import User
from app.layers.models.solicitud_proveedor import SolicitudProveedor, SolicitudProveedorCreate, SolicitudRevision
from app.layers.business.solicitud_proveedor_service import SolicitudProveedorService

router = APIRouter(prefix="/solicitudes-proveedor", tags=["Flujo del Proveedor"])

@router.post("/", response_model=SolicitudProveedor)
def crear_solicitud(
    data: SolicitudProveedorCreate, 
    db: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user)
):
    return SolicitudProveedorService.crear_solicitud(db, data, usuario_actual)

# ¡ESTE FUE EL GET QUE ME FALTÓ PONER LA VEZ PASADA!
@router.get("/", response_model=List[SolicitudProveedor], dependencies=[Depends(require_role(2))])
def listar_solicitudes(db: Session = Depends(get_session)):
    return SolicitudProveedorService.listar_todas(db)

@router.put("/{id_sp}/revision", dependencies=[Depends(require_role(2))])
def revisar_solicitud(
    id_sp: int, 
    data: SolicitudRevision, 
    db: Session = Depends(get_session)
):
    return SolicitudProveedorService.revisar_solicitud(db, id_sp, data)