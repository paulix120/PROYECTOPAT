from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.ciudad import Ciudad

class CiudadRepository:
    @staticmethod
    def obtener_todas(db: Session) -> List[Ciudad]:
        return db.exec(select(Ciudad)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_cdad: int) -> Optional[Ciudad]:
        return db.get(Ciudad, id_cdad)

    @staticmethod
    def obtener_por_departamento(db: Session, id_depart: int) -> List[Ciudad]:
        return db.exec(select(Ciudad).where(Ciudad.id_depart == id_depart)).all()