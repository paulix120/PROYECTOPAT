from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.trayecto import Trayecto
from app.layers.data.base_repository import BaseRepository

class TrayectoRepository:
    @staticmethod
    def obtener_todos(db: Session) -> List[Trayecto]:
        return db.exec(select(Trayecto)).all()

    @staticmethod
    def obtener_por_id(db: Session, id_tray: int) -> Optional[Trayecto]:
        return db.get(Trayecto, id_tray)

    @staticmethod
    def crear_o_actualizar(db: Session, trayecto: Trayecto) -> Trayecto:
        return BaseRepository.guardar(db, trayecto)

    @staticmethod
    def eliminar_fisico(db: Session, trayecto: Trayecto):
        db.delete(trayecto)
        db.commit()