from typing import Optional
from sqlmodel import Field, SQLModel

class Departamento(SQLModel, table=True):
    __tablename__ = "departamento"
    
    id_depart: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    id_pais: int

# DTO para la respuesta del API
class DepartamentoResponse(SQLModel):
    id_depart: int
    nombre: str
    id_pais: int