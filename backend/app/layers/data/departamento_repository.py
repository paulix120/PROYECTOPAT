from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.departamento import Departamento

class DepartamentoRepository:
    @staticmethod
    def obtener_todos(db: Session) -> List[Departamento]:
        return db.exec(select(Departamento)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_depart: int) -> Optional[Departamento]:
        return db.get(Departamento, id_depart)

    @staticmethod
    def obtener_por_pais(db: Session, id_pais: int) -> List[Departamento]:
        return db.exec(select(Departamento).where(Departamento.id_pais == id_pais)).all()