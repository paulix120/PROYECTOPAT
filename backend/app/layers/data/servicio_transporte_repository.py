from sqlmodel import Session, select
from app.layers.models.servicio import Servicio
from app.layers.models.servicio_transporte import ServicioTransporte

class ServicioTransporteRepository:
    @staticmethod
    def listar(db: Session):
        return db.exec(select(Servicio, ServicioTransporte).join(ServicioTransporte, Servicio.id_servicio == ServicioTransporte.id_servicio).where(Servicio.activo == True)).all()

    @staticmethod
    def obtener_padre(db: Session, id_servicio: int):
        return db.get(Servicio, id_servicio)

    @staticmethod
    def obtener_hijo(db: Session, id_servicio: int):
        return db.exec(select(ServicioTransporte).where(ServicioTransporte.id_servicio == id_servicio)).first()