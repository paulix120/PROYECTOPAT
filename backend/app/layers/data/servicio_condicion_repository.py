from sqlmodel import Session, select
from app.layers.models.servicio_condicion import ServicioCondicion

class ServicioCondicionRepository:
    @staticmethod
    def crear(db: Session, relacion: ServicioCondicion) -> ServicioCondicion:
        db.add(relacion)
        db.commit()
        db.refresh(relacion)
        return relacion

    @staticmethod
    def obtener_por_id(db: Session, id_servicio_condi: int) -> ServicioCondicion:
        return db.get(ServicioCondicion, id_servicio_condi)

    @staticmethod
    def eliminar(db: Session, relacion: ServicioCondicion):
        db.delete(relacion)
        db.commit()