from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.proveedor import Proveedor, ProveedorTpServicio

class ProveedorRepository:
    @staticmethod
    def crear(db: Session, proveedor: Proveedor) -> Proveedor:
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)
        return proveedor

    @staticmethod
    def agregar_servicio_autorizado(db: Session, prov_serv: ProveedorTpServicio):
        db.add(prov_serv)
        db.commit()

    @staticmethod
    def obtener_todos(db: Session) -> List[Proveedor]:
        return db.exec(select(Proveedor)).all()

    # ¡ESTE ES EL MÉTODO QUE FALTABA PARA LOS PROVEEDORES!
    @staticmethod
    def obtener_por_id(db: Session, id_prov: int) -> Optional[Proveedor]:
        return db.get(Proveedor, id_prov)