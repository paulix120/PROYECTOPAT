from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.layers.models.proveedor import Proveedor
from app.layers.business.proveedor_service import ProveedorService

router = APIRouter(prefix="/proveedores", tags=["Flujo del Proveedor"])

@router.get("/", response_model=List[Proveedor])
def listar_proveedores(db: Session = Depends(get_session)):
    return ProveedorService.obtener_todos(db)

@router.get("/{id_prov}", response_model=Proveedor)
def obtener_proveedor(id_prov: int, db: Session = Depends(get_session)):
    return ProveedorService.obtener_por_id(db, id_prov)