from typing import Optional, List
from sqlmodel import Field, SQLModel

class ServicioGastronomia(SQLModel, table=True):
    __tablename__ = "servicio_gastronomia"

    id_gast: Optional[int] = Field(default=None, primary_key=True)
    id_servicio: int = Field(foreign_key="servicio.id_servicio", index=True)
    nom_platillo_menu: str = Field(max_length=100)
    porciones: int = Field(default=1)
    vlr_estimado: float
    horario_atencion: Optional[str] = Field(default=None, max_length=100)

class RestauranteBaseCreate(SQLModel):
    nombre: str
    descripcion: str
    id_tp_turi: int
    id_gama: int
    id_ubi: int

class PlatoGastronomiaCreate(SQLModel):
    nom_platillo_menu: str
    porciones: Optional[int] = 1
    vlr_estimado: float
    horario_atencion: Optional[str] = None

class RestauranteBaseUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_tp_turi: Optional[int] = None
    id_gama: Optional[int] = None
    id_ubi: Optional[int] = None

class PlatoGastronomiaUpdate(SQLModel):
    nom_platillo_menu: Optional[str] = None
    porciones: Optional[int] = None
    vlr_estimado: Optional[float] = None
    horario_atencion: Optional[str] = None

class PlatoGastronomiaResponse(SQLModel):
    id_gast: int
    id_servicio: int
    nom_platillo_menu: str
    porciones: int
    vlr_estimado: float
    horario_atencion: Optional[str] = None

class RestauranteConMenuResponse(SQLModel):
    id_servicio: int
    nombre: str
    descripcion: str
    id_tp_serv: int
    id_tp_turi: int
    id_gama: int
    id_prov: Optional[int] = None
    id_ubi: int
    disponibilidad: bool
    activo: bool
    menu_disponible: List[PlatoGastronomiaResponse] = []