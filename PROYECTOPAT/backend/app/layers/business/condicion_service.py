from sqlmodel import Session
from fastapi import HTTPException, status
from app.layers.data.condicion_repository import CondicionRepository
from app.layers.models.condicion import Condiciones, CondicionCreate, CondicionUpdate
from app.layers.models.politica import Politica 

class CondicionService:
    @staticmethod
    def crear_condicion(db: Session, data: CondicionCreate):
        politica = db.get(Politica, data.id_poli)
        if not politica:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La política asignada no existe.")

        nueva_condicion = Condiciones(
            nombre=data.nombre,
            descripcion=data.descripcion,
            tipo=data.tipo,
            estado="ACTIVA",
            id_poli=data.id_poli
        )
        return CondicionRepository.crear_o_actualizar(db, nueva_condicion)

    @staticmethod
    def listar_condiciones(db: Session):
        return CondicionRepository.obtener_todas(db)

    @staticmethod
    def actualizar_condicion(db: Session, id_condi: int, data: CondicionUpdate):
        condicion = CondicionRepository.obtener_por_id(db, id_condi)
        if not condicion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condición no encontrada.")

        if data.id_poli is not None:
            politica = db.get(Politica, data.id_poli)
            if not politica:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La nueva política asignada no existe.")
        
        datos = data.model_dump(exclude_unset=True)
        for key, value in datos.items():
            setattr(condicion, key, value)
            
        return CondicionRepository.crear_o_actualizar(db, condicion)

    @staticmethod
    def eliminar_condicion(db: Session, id_condi: int):
        condicion = CondicionRepository.obtener_por_id(db, id_condi)
        if not condicion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condición no encontrada.")
        
        condicion.estado = "INACTIVA"
        CondicionRepository.crear_o_actualizar(db, condicion)
        return {"mensaje": "Condición inactivada con éxito."}