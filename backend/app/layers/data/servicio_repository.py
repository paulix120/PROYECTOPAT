from typing import List
from sqlmodel import Session, select
from app.layers.models.servicio import Servicio, ServicioHospedaje

class ServicioRepository:
    
    @staticmethod
    def crear_servicio_base(db: Session, servicio: Servicio) -> Servicio:
        db.add(servicio)
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def agregar_espacio(db: Session, espacio: ServicioHospedaje) -> ServicioHospedaje:
        db.add(espacio)
        db.commit()
        db.refresh(espacio)
        return espacio
        
    @staticmethod
    def obtener_hoteles(db: Session) -> List[Servicio]:
        return db.exec(select(Servicio).where(Servicio.id_tp_serv == 1, Servicio.activo == True)).all()

    @staticmethod
    def obtener_espacios_de_hotel(db: Session, id_servicio: int) -> List[ServicioHospedaje]:
        return db.exec(select(ServicioHospedaje).where(ServicioHospedaje.id_servicio == id_servicio)).all()

    @staticmethod
    def obtener_servicio_por_id(db: Session, id_servicio: int):
        return db.get(Servicio, id_servicio)

    # --- NUEVOS MÉTODOS PARA PUT Y DELETE ---

    @staticmethod
    def obtener_espacio_por_id(db: Session, id_hosp: int):
        return db.get(ServicioHospedaje, id_hosp)

    @staticmethod
    def actualizar(db: Session, objeto):
        db.add(objeto)
        db.commit()
        db.refresh(objeto)
        return objeto

    @staticmethod
    def eliminar_espacio(db: Session, espacio: ServicioHospedaje):
        db.delete(espacio)
        db.commit()