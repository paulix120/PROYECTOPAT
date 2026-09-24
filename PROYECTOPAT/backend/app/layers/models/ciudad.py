from typing import Optional
from sqlmodel import Field, SQLModel

class Ciudad(SQLModel, table=True):
    __tablename__ = "ciudad"
    
    id_cdad: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    id_depart: int

# DTO para la respuesta del API
class CiudadResponse(SQLModel):
    id_cdad: int
    nombre: str
    id_depart: int