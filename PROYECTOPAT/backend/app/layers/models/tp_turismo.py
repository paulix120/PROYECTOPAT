from typing import Optional
from sqlmodel import Field, SQLModel

class TpTurismo(SQLModel, table=True):
    __tablename__ = "tp_turismo"

    id_tp_turi: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: Optional[str] = None