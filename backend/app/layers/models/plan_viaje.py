from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import Field, SQLModel

class PlanViaje(SQLModel, table=True):
    __tablename__ = "plan_viaje"
    id_plan_viaje: Optional[int] = Field(default=None, primary_key=True)
    nombre_plan: str
    fecha_inicio: date
    fecha_fin: date
    costo_total_estimado: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    estado: str = Field(default="DESEO")
    created_at: Optional[datetime] = None
    id_usu: int

class DetPlanViaje(SQLModel, table=True):
    __tablename__ = "det_plan_viaje"
    id_det_plan: Optional[int] = Field(default=None, primary_key=True)
    id_plan_viaje: int
    id_servicio: Optional[int] = None 
    tipo_item: str 
    id_item_especifico: Optional[int] = None 
    cantidad: int = Field(default=1) 
    fecha_servicio: date
    costo_unitario_calculado: Decimal = Field(max_digits=10, decimal_places=2)
    subtotal_calculado: Decimal = Field(max_digits=10, decimal_places=2)
    tiempo_estimado_min: int = Field(default=0) # NUEVO CAMPO
    observaciones: Optional[str] = None

class PlanViajeCreate(SQLModel):
    nombre_plan: str
    fecha_inicio: date
    fecha_fin: date

class ItemViajeCreate(SQLModel):
    id_servicio: Optional[int] = None
    tipo_item: str
    id_item_especifico: Optional[int] = None
    cantidad: int = 1
    fecha_servicio: date
    observaciones: Optional[str] = None
    id_ubicacion_origen: Optional[int] = None 
    id_ubicacion_destino: Optional[int] = None