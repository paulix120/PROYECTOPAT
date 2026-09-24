from typing import List
from sqlmodel import Session, select
from app.layers.models.servicio_imagen import ServicioImagen

class ServicioImagenRepository:
    @staticmethod
    def crear(db: Session, imagen: ServicioImagen) -> ServicioImagen:
        db.add(imagen)
        db.commit()
        db.refresh(imagen)
        return imagen

    @staticmethod
    def obtener_por_servicio(db: Session, id_servicio: int) -> List[ServicioImagen]:
        return db.exec(select(ServicioImagen).where(ServicioImagen.id_servicio == id_servicio)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_img: int) -> ServicioImagen:
        return db.get(ServicioImagen, id_img)

    @staticmethod
    def eliminar(db: Session, imagen: ServicioImagen):
        db.delete(imagen)
        db.commit()