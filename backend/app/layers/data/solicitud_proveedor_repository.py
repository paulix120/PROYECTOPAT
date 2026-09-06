from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.solicitud_proveedor import SolicitudProveedor, SolicitudTpServicio

class SolicitudProveedorRepository:
    @staticmethod
    def crear(db: Session, solicitud: SolicitudProveedor) -> SolicitudProveedor:
        db.add(solicitud)
        db.commit()
        db.refresh(solicitud)
        return solicitud

    @staticmethod
    def agregar_servicio_solicitado(db: Session, sol_serv: SolicitudTpServicio):
        db.add(sol_serv)
        db.commit()

    @staticmethod
    def obtener_por_id(db: Session, id_sp: int) -> Optional[SolicitudProveedor]:
        return db.get(SolicitudProveedor, id_sp)

    # ¡ESTE ES EL MÉTODO QUE FALTABA!
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
    def actualizar(db: Session, solicitud: SolicitudProveedor) -> SolicitudProveedor:
        db.add(solicitud)
        db.commit()
        db.refresh(solicitud)
        return solicitud