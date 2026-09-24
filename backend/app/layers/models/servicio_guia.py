from typing import Optional
from sqlmodel import Field, SQLModel

class ServicioGuia(SQLModel, table=True):
    __tablename__ = "servicio_guia"
    id_guia: Optional[int] = Field(default=None, primary_key=True)
    id_servicio: int = Field(foreign_key="servicio.id_servicio", index=True)
    nombre_tour: str
    vlr_tour: float
    duracion_horas: int
    capacidad_grupo: int
    dificultad: str = Field(default="MEDIA")
    horario: Optional[str] = None

class GuiaCreate(SQLModel):
    nombre: str
    descripcion: str
    id_tp_turi: int
    id_gama: int
    id_ubi: int
    nombre_tour: str
    vlr_tour: float
    duracion_horas: int
    capacidad_grupo: int
    dificultad: str = "MEDIA"
    horario: Optional[str] = None

class GuiaUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_tp_turi: Optional[int] = None
    id_gama: Optional[int] = None
    id_ubi: Optional[int] = None
    nombre_tour: Optional[str] = None
    vlr_tour: Optional[float] = None
    duracion_horas: Optional[int] = None
    capacidad_grupo: Optional[int] = None
    dificultad: Optional[str] = None
    horario: Optional[str] = None