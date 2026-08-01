from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import Field, SQLModel

class Departamento(SQLModel, table=True):
    __tablename__ = "departamentos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

class Ciudad(SQLModel, table=True):
    __tablename__ = "ciudades"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    departamento_id: int = Field(foreign_key="departamentos.id")

class TipoTurismo(SQLModel, table=True):
    __tablename__ = "tipos_turismo"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None

# --- MODELO BASE DE DESTINOS TURÍSTICOS ---
class Destino(SQLModel, table=True):
    __tablename__ = "destinos_turisticos"  # Nombre exacto de tu tabla MySQL

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    ciudad_id: int = Field(foreign_key="ciudades.id")
    tipo_turismo_id: Optional[int] = Field(default=None, foreign_key="tipos_turismo.id")
    latitud: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=8)
    longitud: Optional[Decimal] = Field(default=None, max_digits=11, decimal_places=8)
    direccion: Optional[str] = None
    precio_entrada: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    calificacion_promedio: Decimal = Field(default=Decimal("0.00"), max_digits=3, decimal_places=2)
    total_resenas: int = Field(default=0)
    activo: bool = Field(default=True)
    imagen_principal: Optional[str] = None
    created_at: Optional[datetime] = Field(default=None)


# Esquema para responder datos al Frontend
class DestinoResponse(SQLModel):
    id: int
    nombre: str
    descripcion: str
    ciudad_id: int
    tipo_turismo_id: Optional[int] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    precio_entrada: Decimal
    calificacion_promedio: Decimal
    total_resenas: int
    activo: bool
    imagen_principal: Optional[str] = None


# Esquema para la creación de un nuevo destino
class DestinoCreate(SQLModel):
    nombre: str
    descripcion: str
    ciudad_id: int
    tipo_turismo_id: Optional[int] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    precio_entrada: Optional[Decimal] = Decimal("0.00")
    imagen_principal: Optional[str] = None


# Esquema para la actualización parcial
class DestinoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    ciudad_id: Optional[int] = None
    tipo_turismo_id: Optional[int] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None
    precio_entrada: Optional[Decimal] = None
    activo: Optional[bool] = None
    imagen_principal: Optional[str] = None