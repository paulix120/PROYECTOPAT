from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.solicitud_proveedor import SolicitudProveedor, SolicitudTpServicio


class SolicitudProveedorRepository:
    @staticmethod
    def crear(db: Session, solicitud: SolicitudProveedor, commit: bool = True) -> SolicitudProveedor:
        db.add(solicitud)
        if commit:
            db.commit()
            db.refresh(solicitud)
        else:
            db.flush()
        return solicitud

    @staticmethod
    def agregar_servicio_solicitado(db: Session, sol_serv: SolicitudTpServicio, commit: bool = True):
        db.add(sol_serv)
        if commit:
            db.commit()
        else:
            db.flush()

    @staticmethod
    def obtener_por_id(db: Session, id_sp: int) -> Optional[SolicitudProveedor]:
        return db.get(SolicitudProveedor, id_sp)

    @staticmethod
    def obtener_todas(db: Session) -> List[SolicitudProveedor]:
        return db.exec(select(SolicitudProveedor)).all()

    @staticmethod
    def obtener_servicios_de_solicitud(db: Session, id_sp: int) -> List[SolicitudTpServicio]:
        return db.exec(select(SolicitudTpServicio).where(SolicitudTpServicio.id_sp == id_sp)).all()

    @staticmethod
    def obtener_por_usuario(db: Session, id_usu: int) -> List[SolicitudProveedor]:
        return db.exec(select(SolicitudProveedor).where(SolicitudProveedor.id_usu == id_usu)).all()

    @staticmethod
    def obtener_por_nit(db: Session, nit: str) -> Optional[SolicitudProveedor]:
        return db.exec(select(SolicitudProveedor).where(SolicitudProveedor.nit == nit)).first()

    @staticmethod
    def actualizar(db: Session, solicitud: SolicitudProveedor, commit: bool = True) -> SolicitudProveedor:
        db.add(solicitud)
        if commit:
            db.commit()
            db.refresh(solicitud)
        else:
            db.flush()
        return solicitud