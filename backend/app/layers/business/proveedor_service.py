from fastapi import HTTPException, status
from sqlmodel import Session
from app.layers.data.proveedor_repository import ProveedorRepository

class ProveedorService:
    @staticmethod
    def obtener_todos(db: Session):
        return ProveedorRepository.obtener_todos(db)

    @staticmethod
    def obtener_por_id(db: Session, id_prov: int):
        proveedor = ProveedorRepository.obtener_por_id(db, id_prov)
        if not proveedor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado.")
        return proveedor