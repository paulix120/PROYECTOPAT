from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.tp_turismo import TpTurismo

class TpTurismoRepository:
    @staticmethod
    def obtener_todos(db: Session) -> List[TpTurismo]:
        return db.exec(select(TpTurismo)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_tp_turi: int) -> Optional[TpTurismo]:
        return db.get(TpTurismo, id_tp_turi)