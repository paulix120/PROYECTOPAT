from sqlmodel import Session
from fastapi import HTTPException, status
from app.layers.data.politica_repository import PoliticaRepository
from app.layers.models.politica import Politica, PoliticaCreate, PoliticaUpdate

class PoliticaService:
    @staticmethod
    def crear_politica(db: Session, data: PoliticaCreate):
        nueva_politica = Politica(
            nombre=data.nombre,
            descripcion=data.descripcion,
            estado="ACTIVA"
        )
        return PoliticaRepository.crear_o_actualizar(db, nueva_politica)

    @staticmethod
    def listar_politicas(db: Session):
        return PoliticaRepository.obtener_todas(db)

    @staticmethod
    def actualizar_politica(db: Session, id_poli: int, data: PoliticaUpdate):
        politica = PoliticaRepository.obtener_por_id(db, id_poli)
        if not politica:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Política no encontrada.")
        
        datos = data.model_dump(exclude_unset=True)
        for key, value in datos.items():
            setattr(politica, key, value)
            
        return PoliticaRepository.crear_o_actualizar(db, politica)

    @staticmethod
    def eliminar_politica(db: Session, id_poli: int):
        politica = PoliticaRepository.obtener_por_id(db, id_poli)
        if not politica:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Política no encontrada.")
        
        # Borrado Lógico: Cambiamos el estado a INACTIVA
        politica.estado = "INACTIVA"
        PoliticaRepository.crear_o_actualizar(db, politica)
        return {"mensaje": "Política inactivada con éxito."}