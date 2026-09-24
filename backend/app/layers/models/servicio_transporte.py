from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class ServicioTransporte(SQLModel, table=True):
    __tablename__ = "servicio_transporte"
    id_trans: Optional[int] = Field(default=None, primary_key=True)
    id_servicio: int = Field(foreign_key="servicio.id_servicio", index=True) 
    tipo_vehiculo: str
    capacidad_pasajeros: int
    vlr_km: float
    tarifa_base: float
    horario_servicio: Optional[str] = None
    
    # NUEVOS CAMPOS AÑADIDOS
    es_ruta_programada: bool = Field(default=False)
    id_origen: Optional[int] = None
    id_destino: Optional[int] = None
    fecha_salida: Optional[datetime] = None

class TransporteCreate(SQLModel):
    nombre: str
    descripcion: str
    id_tp_turi: int
    id_gama: int
    id_ubi: int
    tipo_vehiculo: str
    capacidad_pasajeros: int
    vlr_km: float
    tarifa_base: float
    horario_servicio: Optional[str] = None
    es_ruta_programada: bool = False
    id_origen: Optional[int] = None
    id_destino: Optional[int] = None
    fecha_salida: Optional[datetime] = None

class TransporteUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_tp_turi: Optional[int] = None
    id_gama: Optional[int] = None
    id_ubi: Optional[int] = None
    tipo_vehiculo: Optional[str] = None
    capacidad_pasajeros: Optional[int] = None
    vlr_km: Optional[float] = None
    tarifa_base: Optional[float] = None
    horario_servicio: Optional[str] = None
    es_ruta_programada: Optional[bool] = None
    id_origen: Optional[int] = None
    id_destino: Optional[int] = None
    fecha_salida: Optional[datetime] = None