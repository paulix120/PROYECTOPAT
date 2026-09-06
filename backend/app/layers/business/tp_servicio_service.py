from fastapi import HTTPException, status
from sqlmodel import Session
from app.layers.data.tp_servicio_repository import TpServicioRepository

class TpServicioService:
    @staticmethod
    def obtener_todos(db: Session):
        return TpServicioRepository.obtener_todos(db)

    @staticmethod
    def obtener_por_id(db: Session, id_tp_serv: int):
        resultado = TpServicioRepository.obtener_por_id(db, id_tp_serv)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El tipo de servicio especificado no existe."
            )
        return resultado