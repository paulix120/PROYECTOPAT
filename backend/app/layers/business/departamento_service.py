from sqlmodel import Session
from fastapi import HTTPException, status
from app.layers.data.departamento_repository import DepartamentoRepository

class DepartamentoService:
    @staticmethod
    def listar_departamentos(db: Session):
        departamentos = DepartamentoRepository.obtener_todos(db)
        if not departamentos:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron departamentos registrados.")
        return departamentos

    @staticmethod
    def obtener_departamento(db: Session, id_depart: int):
        departamento = DepartamentoRepository.obtener_por_id(db, id_depart)
        if not departamento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El departamento con ID {id_depart} no existe.")
        return departamento

    @staticmethod
    def listar_por_pais(db: Session, id_pais: int):
        departamentos = DepartamentoRepository.obtener_por_pais(db, id_pais)
        if not departamentos:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron departamentos para el país con ID {id_pais}.")
        return departamentos