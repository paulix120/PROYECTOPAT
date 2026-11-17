from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.proveedor import Proveedor, ProveedorTpServicio


class ProveedorRepository:
    @staticmethod
    def crear(db: Session, proveedor: Proveedor, commit: bool = True) -> Proveedor:
        db.add(proveedor)
        if commit:
            db.commit()
            db.refresh(proveedor)
        else:
            db.flush()
        return proveedor

    @staticmethod
    def agregar_servicio_autorizado(db: Session, prov_serv: ProveedorTpServicio, commit: bool = True):
        db.add(prov_serv)
        if commit:
            db.commit()
        else:
            db.flush()

    @staticmethod
    def obtener_todos(db: Session) -> List[Proveedor]:
        return db.exec(select(Proveedor)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_prov: int) -> Optional[Proveedor]:
        return db.get(Proveedor, id_prov)

    @staticmethod
    def obtener_por_usuario(db: Session, id_usu: int) -> Optional[Proveedor]:
        return db.exec(select(Proveedor).where(Proveedor.id_usu == id_usu)).first()