from typing import Optional
from sqlmodel import Field, SQLModel

class DetalleResena(SQLModel, table=True):
    __tablename__ = "detalle_resenas"
    
    id_detalle_resena: Optional[int] = Field(default=None, primary_key=True)
    id_resena: int = Field(foreign_key="resenas.id_resena")
    criterio: str
    calificacion: float

class DetalleResenaCreate(SQLModel):
    id_resena: int
    criterio: str
    calificacion: float

class DetalleResenaUpdate(SQLModel):
    criterio: Optional[str] = None
    calificacion: Optional[float] = None

class DetalleResenaResponse(SQLModel):
    id_detalle_resena: int
    id_resena: int
    criterio: str
    calificacion: float