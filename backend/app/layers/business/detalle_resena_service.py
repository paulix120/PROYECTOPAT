from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session

from app.layers.data.detalle_resena_repository import DetalleResenaRepository
from app.layers.data.resena_repository import ResenaRepository
from app.layers.models.detalle_resena import (
    DetalleResena, DetalleResenaCreate, DetalleResenaUpdate,
)

class DetalleResenaService:

    @staticmethod
    def _validar_rango_calificacion(calificacion: float) -> None:
        if calificacion < 1.0 or calificacion > 5.0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La calificación del criterio debe estar entre 1.0 y 5.0.")

    @staticmethod
    def _validar_criterio(criterio: str) -> str:
        criterio_limpio = criterio.strip()
        if not criterio_limpio:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del criterio no puede estar vacío.")
        return criterio_limpio

    @staticmethod
    def _validar_existencia_resena(db: Session, id_resena: int) -> None:
        resena = ResenaRepository.obtener_por_id(db, id_resena)
        if not resena:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La reseña principal con ID {id_resena} no existe.")

    @classmethod
    def crear_detalle(cls, db: Session, data: DetalleResenaCreate) -> DetalleResena:
        cls._validar_rango_calificacion(data.calificacion)
        criterio_limpio = cls._validar_criterio(data.criterio)
        cls._validar_existencia_resena(db, data.id_resena)

        nuevo_detalle = DetalleResena(
            id_resena=data.id_resena,
            criterio=criterio_limpio,
            calificacion=round(float(data.calificacion), 1)
        )
        return DetalleResenaRepository.crear(db, nuevo_detalle)

    @staticmethod
    def obtener_por_id(db: Session, id_detalle: int) -> DetalleResena:
        detalle = DetalleResenaRepository.obtener_por_id(db, id_detalle)
        if not detalle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Detalle con ID {id_detalle} no encontrado.")
        return detalle

    @classmethod
    def listar_por_resena(cls, db: Session, id_resena: int) -> List[DetalleResena]:
        cls._validar_existencia_resena(db, id_resena)
        return DetalleResenaRepository.obtener_por_resena(db, id_resena)

    @classmethod
    def actualizar_detalle(cls, db: Session, id_detalle: int, data: DetalleResenaUpdate) -> DetalleResena:
        detalle = cls.obtener_por_id(db, id_detalle)

        if data.calificacion is not None:
            cls._validar_rango_calificacion(data.calificacion)
            detalle.calificacion = round(float(data.calificacion), 1)

        if data.criterio is not None:
            detalle.criterio = cls._validar_criterio(data.criterio)

        return DetalleResenaRepository.actualizar(db, detalle)

    @classmethod
    def eliminar_detalle(cls, db: Session, id_detalle: int) -> dict:
        detalle = cls.obtener_por_id(db, id_detalle)
        DetalleResenaRepository.eliminar(db, detalle)
        return {"mensaje": f"Detalle de reseña con ID {id_detalle} eliminado exitosamente."}