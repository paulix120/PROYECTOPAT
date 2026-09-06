from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.condicion import Condiciones
from app.layers.data.base_repository import BaseRepository

class CondicionRepository:
    @staticmethod
    def obtener_todas(db: Session) -> List[Condiciones]:
        return db.exec(select(Condiciones)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_condi: int) -> Optional[Condiciones]:
        return db.get(Condiciones, id_condi)

    @staticmethod
    def crear_o_actualizar(db: Session, condicion: Condiciones) -> Condiciones:
        return BaseRepository.guardar(db, condicion)