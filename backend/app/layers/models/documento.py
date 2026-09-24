from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Documento(SQLModel, table=True):
    __tablename__ = "documentos"
    
    id_doc: Optional[int] = Field(default=None, primary_key=True)
    id_usu: int
    id_sp: Optional[int] = None
    tipo_doc: str
    nom_archivo: str
    ruta_archivo: str
    fecha_carga: Optional[datetime] = None
    estado: str = Field(default="PENDIENTE") # PENDIENTE, APROBADO, RECHAZADO