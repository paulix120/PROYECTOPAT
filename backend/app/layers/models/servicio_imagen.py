from typing import Optional
from sqlmodel import Field, SQLModel

class ServicioImagen(SQLModel, table=True):
    __tablename__ = "servicio_imagen"
    id_img: Optional[int] = Field(default=None, primary_key=True)
    id_servicio: int = Field(index=True)
    ruta_url: str
    tipo_arch: str
    es_principal: bool = Field(default=False)