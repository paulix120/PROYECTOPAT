from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel

# Modelos Base de Datos
class SolicitudProveedor(SQLModel, table=True):
    __tablename__ = "solicitud_proveedor"
    id_sp: Optional[int] = Field(default=None, primary_key=True)
    id_usu: int
    nit: str = Field(unique=True)
    razon_social: str
    telefono_contacto: str
    cuenta_bancaria: str
    banco: str
    estado: str = Field(default="EN_REVISION")
    fecha_solicitud: Optional[datetime] = None
    observaciones: Optional[str] = None

class SolicitudTpServicio(SQLModel, table=True):
    __tablename__ = "solicitud_tp_servicio"
    id_sol_serv: Optional[int] = Field(default=None, primary_key=True)
    id_sp: int
    id_tp_serv: int

# DTOs
class SolicitudProveedorCreate(SQLModel):
    nit: str
    razon_social: str
    telefono_contacto: str
    cuenta_bancaria: str
    banco: str
    tipos_servicio_ids: List[int] # ¡AQUÍ JUAN MANDA LA LISTA DE SERVICIOS QUE QUIERE! (Ej: [1, 4])

class SolicitudRevision(SQLModel):
    estado: str 
    observaciones: Optional[str] = None