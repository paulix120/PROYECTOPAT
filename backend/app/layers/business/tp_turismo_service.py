from fastapi import HTTPException, status
from sqlmodel import Session
from app.layers.data.tp_turismo_repository import TpTurismoRepository

class TpTurismoService:
    @staticmethod
    def obtener_todos(db: Session):
        return TpTurismoRepository.obtener_todos(db)

    @staticmethod
    def obtener_por_id(db: Session, id_tp_turi: int):
        resultado = TpTurismoRepository.obtener_por_id(db, id_tp_turi)
        if not resultado:
            # Aquí aplicamos la regla: Usar HTTPException en lugar de prints
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El tipo de turismo especificado no existe."
            )
        return resultado