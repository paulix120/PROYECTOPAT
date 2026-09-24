from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.core.security import get_current_user, require_role
from app.layers.models.auth import User
from app.layers.models.servicio_gastronomia import (
    RestauranteBaseCreate, PlatoGastronomiaCreate,
    RestauranteBaseUpdate, PlatoGastronomiaUpdate,
    RestauranteConMenuResponse, PlatoGastronomiaResponse
)
from app.layers.business.servicio_gastronomia_service import ServicioGastronomiaService

router = APIRouter(prefix="/servicios/gastronomia", tags=["Oferta Turística - Gastronomía"])

@router.get("/restaurantes", response_model=List[RestauranteConMenuResponse])
def listar_restaurantes(db: Session = Depends(get_session)):
    return ServicioGastronomiaService.listar_restaurantes_con_menu(db)

@router.get("/restaurantes/{id_servicio}", response_model=RestauranteConMenuResponse)
def obtener_restaurante(id_servicio: int, db: Session = Depends(get_session)):
    return ServicioGastronomiaService.obtener_restaurante_por_id(db, id_servicio)

@router.get("/mis-restaurantes", response_model=List[RestauranteConMenuResponse], dependencies=[Depends(require_role(3))])
def listar_mis_restaurantes(db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGastronomiaService.listar_mis_restaurantes(db, usuario)

@router.post("/restaurantes/base", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(3))])
def crear_restaurante(data: RestauranteBaseCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGastronomiaService.crear_restaurante_base(db, data, usuario)

@router.post("/restaurantes/{id_servicio}/platos", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(3))])
def agregar_plato(id_servicio: int, data: PlatoGastronomiaCreate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGastronomiaService.agregar_plato_comida(db, id_servicio, data, usuario)

@router.put("/restaurantes/base/{id_servicio}", dependencies=[Depends(require_role(3))])
def editar_restaurante(id_servicio: int, data: RestauranteBaseUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGastronomiaService.actualizar_restaurante_base(db, id_servicio, data, usuario)

@router.put("/platos/{id_gast}", dependencies=[Depends(require_role(3))])
def editar_plato(id_gast: int, data: PlatoGastronomiaUpdate, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGastronomiaService.actualizar_plato(db, id_gast, data, usuario)

@router.delete("/restaurantes/base/{id_servicio}", dependencies=[Depends(require_role(3))])
def borrar_restaurante(id_servicio: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGastronomiaService.eliminar_restaurante_base(db, id_servicio, usuario)

@router.delete("/platos/{id_gast}", dependencies=[Depends(require_role(3))])
def borrar_plato(id_gast: int, db: Session = Depends(get_session), usuario: User = Depends(get_current_user)):
    return ServicioGastronomiaService.eliminar_plato(db, id_gast, usuario)