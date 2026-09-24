from sqlmodel import Session, select
from app.layers.models.servicio import Servicio
from app.layers.models.servicio_recreacion import ServicioRecreacion

class ServicioRecreacionRepository:
    @staticmethod
    def listar(db: Session):
        return db.exec(select(Servicio, ServicioRecreacion).join(ServicioRecreacion, Servicio.id_servicio == ServicioRecreacion.id_servicio).where(Servicio.activo == True)).all()

    @staticmethod
    def obtener_padre(db: Session, id_servicio: int):
        return db.get(Servicio, id_servicio)

    @staticmethod
    def obtener_hijo(db: Session, id_servicio: int):
        return db.exec(select(ServicioRecreacion).where(ServicioRecreacion.id_servicio == id_servicio)).first()