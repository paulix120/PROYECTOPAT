from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.core.security import get_current_user
from app.layers.models.auth import User
from app.layers.models.plan_viaje import PlanViajeCreate, ItemViajeCreate, PlanViajeUpdate, ItemViajeUpdate
from app.layers.business.plan_viaje_service import PlanViajeService

router = APIRouter(prefix="/planes-viaje", tags=["Fase 4 - El Carrito y Plan de Viaje"])

@router.post("/")
def crear_plan(data: PlanViajeCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return PlanViajeService.crear_plan(db, data, usuario)

@router.get("/mis-planes")
def ver_mis_planes(db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return PlanViajeService.obtener_mis_planes(db, usuario)

@router.post("/{id_plan}/items")
def agregar_item_al_viaje(id_plan: int, data: ItemViajeCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return PlanViajeService.agregar_item(db, id_plan, data, usuario)

# 👇 IMPORTANTE: estas dos van ANTES de "/{id_plan}" para que no choquen las rutas
@router.put("/items/{id_detalle}")
def editar_item(id_detalle: int, data: ItemViajeUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return PlanViajeService.editar_item(db, id_detalle, data, usuario)

@router.delete("/items/{id_detalle}")
def eliminar_item(id_detalle: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return PlanViajeService.eliminar_item(db, id_detalle, usuario)

@router.put("/{id_plan}")
def editar_plan(id_plan: int, data: PlanViajeUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return PlanViajeService.editar_plan(db, id_plan, data, usuario)

@router.delete("/{id_plan}")
def eliminar_plan(id_plan: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return PlanViajeService.eliminar_plan(db, id_plan, usuario)