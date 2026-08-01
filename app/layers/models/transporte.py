from typing import Optional
from sqlmodel import SQLModel, Field

class MedioTransporteBase(SQLModel):
    nombre: str  # Ej: 'Carro propio', 'Moto', 'Bus intermunicipal'
    velocidad_kmh: float = 60.0  # Velocidad promedio para calcular tiempos
    costo_por_km: float  # Variable CLAVE para el presupuesto (Ej: 400.0)
    icono: Optional[str] = None  # Emoji o clase CSS para el frontend futuro

class MedioTransporte(MedioTransporteBase, table=True):
    __tablename__ = "medios_transporte"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    activo: bool = Field(default=True)

class MedioTransporteCreate(MedioTransporteBase):
    pass

class MedioTransporteResponse(MedioTransporteBase):
    id: int
    activo: bool