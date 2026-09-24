from sqlmodel import Session
from fastapi import HTTPException, status
from app.layers.data.ciudad_repository import CiudadRepository

class CiudadService:
    @staticmethod
    def listar_ciudades(db: Session):
        ciudades = CiudadRepository.obtener_todas(db)
        if not ciudades:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron ciudades registradas.")
        return ciudades

    @staticmethod
    def obtener_ciudad(db: Session, id_cdad: int):
        ciudad = CiudadRepository.obtener_por_id(db, id_cdad)
        if not ciudad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La ciudad con ID {id_cdad} no existe.")
        return ciudad

    @staticmethod
    def listar_por_departamento(db: Session, id_depart: int):
        ciudades = CiudadRepository.obtener_por_departamento(db, id_depart)
        if not ciudades:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron ciudades para el departamento con ID {id_depart}.")
        return ciudades