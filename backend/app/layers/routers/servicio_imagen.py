from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user, require_role
from app.layers.models.auth import User
from app.layers.models.servicio_imagen import ServicioImagen
from app.layers.business.servicio_imagen_service import ServicioImagenService

router = APIRouter(prefix="/servicio-imagenes", tags=["Fase 3 - Imágenes de Servicios"])

# Permitimos Rol 2 (Admin) y Rol 3 (Proveedor)
@router.post("/{id_servicio}", response_model=ServicioImagen, dependencies=[Depends(require_role(2, 3))])
def subir_imagen_servicio(
    id_servicio: int,
    es_principal: bool = Form(False),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user)
):
    return ServicioImagenService.subir_imagen(db, id_servicio, archivo, es_principal, usuario_actual)

@router.delete("/{id_img}", dependencies=[Depends(require_role(2, 3))])
def eliminar_imagen(id_img: int, db: Session = Depends(get_session), usuario_actual: User = Depends(get_current_user)):
    return ServicioImagenService.eliminar_imagen(db, id_img, usuario_actual)