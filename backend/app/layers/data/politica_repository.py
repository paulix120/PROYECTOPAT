from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.politica import Politica
from app.layers.data.base_repository import BaseRepository

class PoliticaRepository:
    @staticmethod
    def obtener_todas(db: Session) -> List[Politica]:
        return db.exec(select(Politica)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_poli: int) -> Optional[Politica]:
        return db.get(Politica, id_poli)

    @staticmethod
    def crear_o_actualizar(db: Session, politica: Politica) -> Politica:
        return BaseRepository.guardar(db, politica)