from typing import Optional
from sqlmodel import Field, SQLModel

class ServicioCondicion(SQLModel, table=True):
    __tablename__ = "servicio_condicion"
    id_servicio_condi: Optional[int] = Field(default=None, primary_key=True)
    id_servicio: int
    id_condi: int

class ServicioCondicionCreate(SQLModel):
    id_servicio: int
    id_condi: int