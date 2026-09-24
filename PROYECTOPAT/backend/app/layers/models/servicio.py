from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

# 1. TABLA PADRE (El Hotel / Alojamiento Principal)
class Servicio(SQLModel, table=True):
    __tablename__ = "servicio"
    id_servicio: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    id_tp_serv: int
    id_tp_turi: int
    id_gama: int
    id_prov: Optional[int] = None
    id_ubi: int
    disponibilidad: bool = Field(default=True)
    activo: bool = Field(default=True)
    fecha_creacion: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# 2. TABLA HIJA (Los Espacios / Habitaciones)
class ServicioHospedaje(SQLModel, table=True):
    __tablename__ = "servicio_hospedaje"
    id_hosp: Optional[int] = Field(default=None, primary_key=True)
    id_servicio: int 
    nom_unidad: str
    capacidad_personas: int
    vlr_noche: float 
    horario_checkin: Optional[str] = None
    horario_checkout: Optional[str] = None

# ==========================================
# DTOS: CREAR
# ==========================================
class HospedajeBaseCreate(SQLModel):
    nombre: str
    descripcion: str
    id_tp_turi: int
    id_gama: int
    id_ubi: int

class HospedajeEspacioCreate(SQLModel):
    nom_unidad: str 
    capacidad_personas: int
    vlr_noche: float
    horario_checkin: str
    horario_checkout: str

# ==========================================
# DTOS: ACTUALIZAR (PUT)
# ==========================================
class HospedajeBaseUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_tp_turi: Optional[int] = None
    id_gama: Optional[int] = None

class HospedajeEspacioUpdate(SQLModel):
    nom_unidad: Optional[str] = None
    capacidad_personas: Optional[int] = None
    vlr_noche: Optional[float] = None
    horario_checkin: Optional[str] = None
    horario_checkout: Optional[str] = None