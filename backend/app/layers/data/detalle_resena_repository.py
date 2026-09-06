from typing import List, Optional
from sqlmodel import Session, select
from app.layers.data.base_repository import BaseRepository
from app.layers.models.detalle_resena import DetalleResena

class DetalleResenaRepository:
    @staticmethod
    def obtener_por_id(db: Session, id_detalle: int) -> Optional[DetalleResena]:
        return BaseRepository.obtener_por_id(db, DetalleResena, id_detalle)

    @staticmethod
    def obtener_por_resena(db: Session, id_resena: int) -> List[DetalleResena]:
        return db.exec(select(DetalleResena).where(DetalleResena.id_resena == id_resena)).all()

    @staticmethod
    def crear(db: Session, detalle: DetalleResena) -> DetalleResena:
        return BaseRepository.guardar(db, detalle)

    @staticmethod
    def actualizar(db: Session, detalle: DetalleResena) -> DetalleResena:
        return BaseRepository.actualizar(db, detalle)

    @staticmethod
    def eliminar(db: Session, detalle: DetalleResena) -> None:
        db.delete(detalle)
        db.commit()