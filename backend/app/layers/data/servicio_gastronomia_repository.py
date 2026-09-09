from typing import List, Optional
from sqlmodel import Session, select
from app.layers.models.servicio import Servicio
from app.layers.models.servicio_gastronomia import ServicioGastronomia

class ServicioGastronomiaRepository:
    @staticmethod
    def crear_restaurante_base(db: Session, servicio: Servicio) -> Servicio:
        db.add(servicio)
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def obtener_restaurantes(db: Session, solo_activos: bool = True) -> List[Servicio]:
        query = select(Servicio).where(Servicio.id_tp_serv == 2)
        if solo_activos:
            query = query.where(Servicio.activo == True)
        return db.exec(query).all()

    @staticmethod
    def obtener_restaurantes_por_proveedor(db: Session, id_prov: int) -> List[Servicio]:
        return db.exec(
            select(Servicio).where(
                Servicio.id_tp_serv == 2, Servicio.id_prov == id_prov, Servicio.activo == True
            )
        ).all()

    @staticmethod
    def obtener_restaurante_por_id(db: Session, id_servicio: int) -> Optional[Servicio]:
        servicio = db.get(Servicio, id_servicio)
        if servicio and servicio.id_tp_serv == 2:
            return servicio
        return None

    @staticmethod
    def agregar_plato(db: Session, plato: ServicioGastronomia) -> ServicioGastronomia:
        db.add(plato)
        db.commit()
        db.refresh(plato)
        return plato

    @staticmethod
    def obtener_platos_de_restaurante(db: Session, id_servicio: int) -> List[ServicioGastronomia]:
        return db.exec(select(ServicioGastronomia).where(ServicioGastronomia.id_servicio == id_servicio)).all()

    @staticmethod
    def obtener_plato_por_id(db: Session, id_gast: int) -> Optional[ServicioGastronomia]:
        return db.get(ServicioGastronomia, id_gast)

    @staticmethod
    def actualizar(db: Session, objeto):
        db.add(objeto)
        db.commit()
        db.refresh(objeto)
        return objeto

    @staticmethod
    def eliminar_plato(db: Session, plato: ServicioGastronomia):
        db.delete(plato)
        db.commit()