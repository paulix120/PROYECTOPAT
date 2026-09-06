from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class EstadoResena(str, Enum):
    ACTIVA = "ACTIVA"
    OCULTA = "OCULTA"
    REPORTADA = "REPORTADA"

class Resena(SQLModel, table=True):
    __tablename__ = "resenas"

    id_resena: Optional[int] = Field(default=None, primary_key=True)
    id_usu: int = Field(foreign_key="usuario.id_usu", index=True)
    id_servicio: int = Field(foreign_key="servicio.id_servicio", index=True)
    clf_general: float = Field(description="Calificación general entre 1.0 y 5.0")
    comentario: Optional[str] = Field(default=None, max_length=1000)
    fecha_resena: Optional[datetime] = Field(default_factory=datetime.utcnow)
    estado: str = Field(default=EstadoResena.ACTIVA.value)

class ResenaCreate(SQLModel):
    id_usu: int
    id_servicio: int
    clf_general: float
    comentario: Optional[str] = None

class ResenaUpdate(SQLModel):
    clf_general: Optional[float] = None
    comentario: Optional[str] = None
    estado: Optional[str] = None

class ResenaResponse(SQLModel):
    id_resena: int
    id_usu: int
    id_servicio: int
    clf_general: float
    comentario: Optional[str] = None
    fecha_resena: Optional[datetime] = None
    estado: str