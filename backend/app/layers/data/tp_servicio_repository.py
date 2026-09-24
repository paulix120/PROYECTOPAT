from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.tp_servicio import TpServicio

class TpServicioRepository:
    @staticmethod
    def obtener_todos(db: Session) -> List[TpServicio]:
        return db.exec(select(TpServicio)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_tp_serv: int) -> Optional[TpServicio]:
        return db.get(TpServicio, id_tp_serv)