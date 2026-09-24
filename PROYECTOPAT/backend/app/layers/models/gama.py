from typing import Optional
from sqlmodel import Field, SQLModel

class Gama(SQLModel, table=True):
    __tablename__ = "gama"

    id_gama: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: str