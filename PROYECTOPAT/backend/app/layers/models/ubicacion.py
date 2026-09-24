from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel

class Ubicacion(SQLModel, table=True):
    __tablename__ = "ubicacion"
    
    id_ubi: Optional[int] = Field(default=None, primary_key=True)
    direccion: str
    barrio: Optional[str] = None
    codigo_postal: Optional[str] = None
    latitud: Decimal = Field(max_digits=10, decimal_places=8)
    longitud: Decimal = Field(max_digits=11, decimal_places=8)
    descripcion: Optional[str] = None
    id_cdad: int
    activo: bool = Field(default=True)

class UbicacionCreate(SQLModel):
    direccion: str
    barrio: Optional[str] = None
    codigo_postal: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    descripcion: Optional[str] = None
    id_cdad: int

class UbicacionUpdate(SQLModel):
    direccion: Optional[str] = None
    barrio: Optional[str] = None
    codigo_postal: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    descripcion: Optional[str] = None
    id_cdad: Optional[int] = None

class UbicacionResponse(Ubicacion):
    pass