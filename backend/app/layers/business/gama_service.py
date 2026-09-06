from fastapi import HTTPException, status
from sqlmodel import Session
from app.layers.data.gama_repository import GamaRepository

class GamaService:
    @staticmethod
    def obtener_todos(db: Session):
        return GamaRepository.obtener_todos(db)

    @staticmethod
    def obtener_por_id(db: Session, id_gama: int):
        resultado = GamaRepository.obtener_por_id(db, id_gama)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La gama especificada no existe."
            )
        return resultado