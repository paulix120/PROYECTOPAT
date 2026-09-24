from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.gama import Gama

class GamaRepository:
    @staticmethod
    def obtener_todos(db: Session) -> List[Gama]:
        return db.exec(select(Gama)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_gama: int) -> Optional[Gama]:
        return db.get(Gama, id_gama)