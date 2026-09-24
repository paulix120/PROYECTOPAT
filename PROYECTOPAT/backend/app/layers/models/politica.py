from typing import Optional
from sqlmodel import Field, SQLModel

class Politica(SQLModel, table=True):
    __tablename__ = "politica"
    
    id_poli: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150)
    descripcion: str
    estado: str = Field(default="ACTIVA") # Valores: 'ACTIVA' o 'INACTIVA'

class PoliticaCreate(SQLModel):
    nombre: str
    descripcion: str

class PoliticaUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None

class PoliticaResponse(Politica):
    pass