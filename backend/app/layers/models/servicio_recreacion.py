from typing import Optional
from sqlmodel import Field, SQLModel

class ServicioRecreacion(SQLModel, table=True):
    __tablename__ = "servicio_recreacion"
    id_rec: Optional[int] = Field(default=None, primary_key=True)
    id_servicio: int = Field(foreign_key="servicio.id_servicio", index=True)
    nom_actividad: str
    duracion: Optional[str] = None
    horario: Optional[str] = None
    vlr_persona: float = Field(default=0.0)
    capacidad: Optional[int] = None
    es_evento_local: bool = Field(default=False)

class RecreacionCreate(SQLModel):
    nombre: str
    descripcion: str
    id_tp_turi: int
    id_gama: int
    id_ubi: int
    nom_actividad: str
    duracion: Optional[str] = None
    horario: Optional[str] = None
    vlr_persona: float = 0.0
    capacidad: Optional[int] = None
    es_evento_local: bool = False

class RecreacionUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_tp_turi: Optional[int] = None
    id_gama: Optional[int] = None
    id_ubi: Optional[int] = None
    nom_actividad: Optional[str] = None
    duracion: Optional[str] = None
    horario: Optional[str] = None
    vlr_persona: Optional[float] = None
    capacidad: Optional[int] = None
    es_evento_local: Optional[bool] = None