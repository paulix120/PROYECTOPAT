from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.ubicacion import Ubicacion
from app.layers.data.base_repository import BaseRepository

class UbicacionRepository:
    @staticmethod
    def obtener_todas(db: Session) -> List[Ubicacion]:
        return db.exec(select(Ubicacion).where(Ubicacion.activo == True)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_ubi: int) -> Optional[Ubicacion]:
        return db.exec(select(Ubicacion).where(Ubicacion.id_ubi == id_ubi, Ubicacion.activo == True)).first()

    @staticmethod
    def crear_o_actualizar(db: Session, ubicacion: Ubicacion) -> Ubicacion:
        return BaseRepository.guardar(db, ubicacion)