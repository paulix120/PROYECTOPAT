from sqlmodel import Session, select
from app.layers.models.plan_viaje import PlanViaje, DetPlanViaje

class PlanViajeRepository:
    @staticmethod
    def crear_plan(db: Session, plan: PlanViaje) -> PlanViaje:
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def obtener_por_id(db: Session, id_plan: int) -> PlanViaje:
        return db.get(PlanViaje, id_plan)

    @staticmethod
    def obtener_por_usuario(db: Session, id_usu: int):
        return db.exec(select(PlanViaje).where(PlanViaje.id_usu == id_usu)).all()

    @staticmethod
    def agregar_detalle(db: Session, detalle: DetPlanViaje) -> DetPlanViaje:
        db.add(detalle)
        db.commit()
        db.refresh(detalle)
        return detalle

    @staticmethod
    def actualizar_plan(db: Session, plan: PlanViaje):
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def obtener_detalles(db: Session, id_plan: int):
        return db.exec(select(DetPlanViaje).where(DetPlanViaje.id_plan_viaje == id_plan)).all()