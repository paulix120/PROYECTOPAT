from typing import Optional
from sqlmodel import Field, SQLModel

class TpServicio(SQLModel, table=True):
    __tablename__ = "tp_servicio"

    id_tp_serv: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: str