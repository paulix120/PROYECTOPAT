from typing import Optional
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel

class Trayecto(SQLModel, table=True):
    __tablename__ = "trayecto"
    
    id_tray: Optional[int] = Field(default=None, primary_key=True)
    id_origen: int
    id_destino: int
    distancia_km: Decimal = Field(max_digits=10, decimal_places=2)
    tiempo_estimado_min: int
    fecha_calculo: Optional[datetime] = Field(default_factory=datetime.utcnow)

class TrayectoCreate(SQLModel):
    id_origen: int
    id_destino: int

class TrayectoUpdate(SQLModel):
    id_origen: Optional[int] = None
    id_destino: Optional[int] = None

class TrayectoResponse(Trayecto):
    pass