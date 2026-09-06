from typing import Optional
from sqlmodel import Field, SQLModel

class Condiciones(SQLModel, table=True):
    __tablename__ = "condiciones"
    
    id_condi: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150)
    descripcion: str
    tipo: str = Field(default="OTRO") # 'CANCELACION', 'RESERVA', 'PAGO', 'USO', 'OTRO'
    estado: str = Field(default="ACTIVA") # 'ACTIVA' o 'INACTIVA'
    id_poli: int

class CondicionCreate(SQLModel):
    nombre: str
    descripcion: str
    tipo: str
    id_poli: int

class CondicionUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None
    id_poli: Optional[int] = None

class CondicionResponse(Condiciones):
    pass