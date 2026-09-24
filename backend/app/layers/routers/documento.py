from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user
from app.layers.models.auth import User
from app.layers.models.documento import Documento
from app.layers.business.documento_service import DocumentoService

router = APIRouter(prefix="/documentos", tags=["Subida de Archivos"])

@router.post("/", response_model=Documento)
def subir_documento(
    tipo_doc: str = Form(..., description="Ej: RUT, RNT, Cedula"),
    id_sp: Optional[int] = Form(None, description="ID de la solicitud (Opcional)"),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user)
):
    return DocumentoService.subir_documento(db, usuario_actual, tipo_doc, archivo, id_sp)

@router.get("/mis-documentos", response_model=List[Documento])
def obtener_mis_documentos(
    db: Session = Depends(get_session),
    usuario_actual: User = Depends(get_current_user)
):
    return DocumentoService.obtener_mis_documentos(db, usuario_actual)