from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Proveedor(SQLModel, table=True):
    __tablename__ = "proveedor"
    id_prov: Optional[int] = Field(default=None, primary_key=True)
    id_usu: int = Field(unique=True)
    id_sp: int = Field(unique=True)
    estado: str = Field(default="ACTIVO")
    fecha_registro: Optional[datetime] = None

class ProveedorTpServicio(SQLModel, table=True):
    __tablename__ = "proveedor_tp_servicio"
    id_prov_serv: Optional[int] = Field(default=None, primary_key=True)
    id_prov: int
    id_tp_serv: int