from typing import Optional
from sqlmodel import Session
from app.layers.models.resena import Resena

class ResenaRepository:
    @staticmethod
    def obtener_por_id(db: Session, id_resena: int) -> Optional[Resena]:
        return db.get(Resena, id_resena)