from sqlmodel import Session, select
from app.layers.models.servicio import Servicio
from app.layers.models.servicio_guia import ServicioGuia

class ServicioGuiaRepository:
    @staticmethod
    def listar(db: Session):
        return db.exec(select(Servicio, ServicioGuia).join(ServicioGuia, Servicio.id_servicio == ServicioGuia.id_servicio).where(Servicio.activo == True)).all()

    @staticmethod
    def obtener_padre(db: Session, id_servicio: int):
        return db.get(Servicio, id_servicio)

    @staticmethod
    def obtener_hijo(db: Session, id_servicio: int):
        return db.exec(select(ServicioGuia).where(ServicioGuia.id_servicio == id_servicio)).first()